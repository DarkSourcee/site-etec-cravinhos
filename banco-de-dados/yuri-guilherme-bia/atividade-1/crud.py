"""
Exercícios de CRUD — Python + MySQL (console)
Instalação:  pip install mysql-connector-python
Antes de rodar, execute o arquivo banco.sql no MySQL e ajuste CONFIG abaixo.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation

import mysql.connector

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "exercicios_crud",
}


# ---------------------------------------------------------------- entrada
def ler_texto(msg):
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("  Valor obrigatório.")


def ler_inteiro(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("  Digite um número inteiro.")


def ler_decimal(msg):
    while True:
        try:
            return Decimal(input(msg).strip().replace(",", "."))
        except InvalidOperation:
            print("  Digite um valor numérico (ex.: 1234.50).")


def ler_data(msg):
    while True:
        try:
            return datetime.strptime(input(msg).strip(), "%d/%m/%Y").date()
        except ValueError:
            print("  Use o formato dd/mm/aaaa.")


# Para cada tabela: (coluna, rótulo, função de leitura)
TABELAS = {
    "alunos": {
        "titulo": "Cadastro de Alunos",
        "singular": "aluno",
        "campos": [
            ("nome", "Nome", ler_texto),
            ("idade", "Idade", ler_inteiro),
            ("curso", "Curso", ler_texto),
        ],
    },
    "produtos": {
        "titulo": "Cadastro de Produtos",
        "singular": "produto",
        "campos": [
            ("nome", "Nome", ler_texto),
            ("preco", "Preço", ler_decimal),
            ("quantidade", "Quantidade", ler_inteiro),
        ],
    },
    "funcionarios": {
        "titulo": "Cadastro de Funcionários",
        "singular": "funcionário",
        "campos": [
            ("nome", "Nome", ler_texto),
            ("cargo", "Cargo", ler_texto),
            ("salario", "Salário", ler_decimal),
            ("data_admissao", "Data de admissão (dd/mm/aaaa)", ler_data),
        ],
    },
}


def formatar(valor):
    if isinstance(valor, Decimal):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if hasattr(valor, "strftime"):
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def mostrar(linhas, tabela):
    if not linhas:
        print("  Nenhum registro encontrado.")
        return
    colunas = ["id"] + [c for c, _, _ in TABELAS[tabela]["campos"]]
    print("  " + " | ".join(c.upper() for c in colunas))
    print("  " + "-" * 60)
    for linha in linhas:
        print("  " + " | ".join(formatar(v) for v in linha))


# ------------------------------------------------------------------- CRUD
def buscar_por_id(cur, tabela, id_):
    cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id_,))
    return cur.fetchone()


def criar(conn, tabela):
    cfg = TABELAS[tabela]
    valores = [ler(f"{rotulo}: ") for _, rotulo, ler in cfg["campos"]]
    colunas = ", ".join(c for c, _, _ in cfg["campos"])
    marcadores = ", ".join(["%s"] * len(valores))
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {tabela} ({colunas}) VALUES ({marcadores})", valores)
    conn.commit()
    print(f"  {cfg['singular'].capitalize()} cadastrado com ID {cur.lastrowid}.")


def listar(conn, tabela):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tabela} ORDER BY id")
    mostrar(cur.fetchall(), tabela)


def atualizar(conn, tabela):
    cfg = TABELAS[tabela]
    cur = conn.cursor()
    id_ = ler_inteiro("ID para atualizar: ")
    atual = buscar_por_id(cur, tabela, id_)
    if not atual:  # verifica se o registro existe
        print(f"  Nenhum {cfg['singular']} com ID {id_}.")
        return
    print("  Registro atual:")
    mostrar([atual], tabela)
    print("  Informe os novos dados (Enter mantém o valor atual).")
    novos = []
    for i, (_, rotulo, ler) in enumerate(cfg["campos"], start=1):
        # Enter vazio mantém o valor; caso contrário, reaproveita a validação
        while True:
            bruto = input(f"{rotulo} [{formatar(atual[i])}]: ").strip()
            if not bruto:
                novos.append(atual[i])
                break
            try:
                novos.append(_converter(ler, bruto))
                break
            except ValueError:
                print("  Valor inválido.")
    sets = ", ".join(f"{c} = %s" for c, _, _ in cfg["campos"])
    cur.execute(f"UPDATE {tabela} SET {sets} WHERE id = %s", novos + [id_])
    conn.commit()
    print("  Registro atualizado.")


def _converter(ler, bruto):
    """Converte um texto usando as mesmas regras das funções de leitura."""
    if ler is ler_texto:
        return bruto
    if ler is ler_inteiro:
        return int(bruto)
    if ler is ler_decimal:
        try:
            return Decimal(bruto.replace(",", "."))
        except InvalidOperation:
            raise ValueError
    if ler is ler_data:
        return datetime.strptime(bruto, "%d/%m/%Y").date()
    raise ValueError


def excluir(conn, tabela):
    cfg = TABELAS[tabela]
    cur = conn.cursor()
    id_ = ler_inteiro("ID para excluir: ")
    registro = buscar_por_id(cur, tabela, id_)
    if not registro:  # verifica se o registro existe
        print(f"  Nenhum {cfg['singular']} com ID {id_}.")
        return
    mostrar([registro], tabela)
    if input("  Confirmar exclusão? (s/n): ").strip().lower() == "s":
        cur.execute(f"DELETE FROM {tabela} WHERE id = %s", (id_,))
        conn.commit()
        print("  Registro excluído.")
    else:
        print("  Exclusão cancelada.")


# ---------------------------------------------------------- desafios extras
def pesquisar_aluno(conn):
    termo = ler_texto("Nome (ou parte): ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos WHERE nome LIKE %s", (f"%{termo}%",))
    mostrar(cur.fetchall(), "alunos")


def estoque_baixo(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM produtos WHERE quantidade < 5 ORDER BY quantidade")
    mostrar(cur.fetchall(), "produtos")


def valor_total_estoque(conn):
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(preco * quantidade), 0) FROM produtos")
    print(f"  Valor total do estoque: {formatar(cur.fetchone()[0])}")


def pesquisar_cargo(conn):
    termo = ler_texto("Cargo (ou parte): ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM funcionarios WHERE cargo LIKE %s", (f"%{termo}%",))
    mostrar(cur.fetchall(), "funcionarios")


def salarios_altos(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM funcionarios WHERE salario > 3000 ORDER BY salario DESC")
    mostrar(cur.fetchall(), "funcionarios")


def media_salarial(conn):
    cur = conn.cursor()
    cur.execute("SELECT AVG(salario) FROM funcionarios")
    media = cur.fetchone()[0]
    print("  Sem funcionários cadastrados." if media is None
          else f"  Média salarial: {formatar(Decimal(media))}")


EXTRAS = {
    "alunos": [("Pesquisar aluno pelo nome", pesquisar_aluno)],
    "produtos": [
        ("Listar produtos com quantidade < 5", estoque_baixo),
        ("Valor total do estoque", valor_total_estoque),
    ],
    "funcionarios": [
        ("Pesquisar por cargo", pesquisar_cargo),
        ("Listar salários > R$ 3.000,00", salarios_altos),
        ("Média salarial", media_salarial),
    ],
}


# ------------------------------------------------------------------- menus
def menu_tabela(conn, tabela):
    cfg = TABELAS[tabela]
    acoes = [
        (f"Cadastrar {cfg['singular']}", criar),
        (f"Listar {tabela}", listar),
        (f"Atualizar {cfg['singular']}", atualizar),
        (f"Excluir {cfg['singular']}", excluir),
    ]
    while True:
        print(f"\n=== {cfg['titulo']} ===")
        for i, (nome, _) in enumerate(acoes, start=1):
            print(f"{i} - {nome}")
        base = len(acoes)
        for j, (nome, _) in enumerate(EXTRAS[tabela], start=base + 1):
            print(f"{j} - [Extra] {nome}")
        print("0 - Voltar")
        op = ler_inteiro("Opção: ")
        if op == 0:
            return
        if 1 <= op <= base:
            acoes[op - 1][1](conn, tabela)
        elif base < op <= base + len(EXTRAS[tabela]):
            EXTRAS[tabela][op - base - 1][1](conn)
        else:
            print("  Opção inválida.")


def main():
    try:
        conn = mysql.connector.connect(**CONFIG)
    except mysql.connector.Error as erro:
        print(f"Não foi possível conectar ao MySQL: {erro}")
        return
    try:
        while True:
            print("\n=== EXERCÍCIOS DE CRUD ===")
            print("1 - Alunos\n2 - Produtos\n3 - Funcionários\n0 - Sair")
            op = ler_inteiro("Opção: ")
            if op == 0:
                break
            if op in (1, 2, 3):
                menu_tabela(conn, ["alunos", "produtos", "funcionarios"][op - 1])
            else:
                print("  Opção inválida.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
