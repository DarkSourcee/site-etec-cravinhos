# Oracle SQL: PK, FK, INNER JOIN e LEFT JOIN

Exercício prático de relacionamento entre tabelas em **Oracle SQL**, usando as tabelas `CLIENTES` e `PEDIDOS`.

## Conceitos

| Conceito | Ideia principal |
|---|---|
| PK | Identifica unicamente um registro |
| FK | Aponta para a PK de outra tabela e cria a ligação |
| JOIN | Combina dados relacionados de tabelas |
| INNER JOIN | Retorna apenas correspondências |
| LEFT JOIN | Mantém todos os registros da tabela da esquerda |
| ON | Define como as tabelas serão relacionadas |
| NULL no LEFT JOIN | Indica que não há correspondência na tabela da direita |

## Modelo

```
CLIENTES (1) ────────< (N) PEDIDOS
---------                  ---------
id_cliente  PK             id_pedido   PK
nome                       id_cliente  FK -> clientes.id_cliente
                           descricao
                           valor
                           data_pedido
```

Um cliente pode ter vários pedidos (relação 1:N). A FK fica na tabela do lado "muitos" (`PEDIDOS`).

## Estrutura do repositório

```
.
├── README.md
├── LICENSE
├── .gitignore
└── sql/
    ├── 00_limpar.sql
    ├── 01_criar_tabelas.sql
    ├── 02_inserir_dados.sql
    ├── 03_consultas.sql
    └── exercicio_completo.sql
```

## Como executar

**Opção 1: tudo de uma vez**

Rode `sql/exercicio_completo.sql`.

**Opção 2: passo a passo**

1. `sql/01_criar_tabelas.sql`
2. `sql/02_inserir_dados.sql`
3. `sql/03_consultas.sql`

> No SQL Developer, use **F5** (Executar Script) para rodar o arquivo inteiro.
> Para recomeçar do zero, rode `sql/00_limpar.sql` antes.

## Consultas do exercício

### 1. Todos os clientes com seus pedidos (LEFT JOIN)

```sql
SELECT c.id_cliente, c.nome, p.id_pedido, p.descricao, p.valor, p.data_pedido
FROM clientes c
LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
ORDER BY c.id_cliente, p.id_pedido;
```

| ID_CLIENTE | NOME | ID_PEDIDO | DESCRICAO | VALOR | DATA_PEDIDO |
|---|---|---|---|---|---|
| 1 | Ana | 101 | Pedido de material | 150,00 | 01/11/2026 |
| 1 | Ana | 102 | Pedido de perfume | 80,00 | 02/11/2026 |
| 2 | Maria | 103 | Pedido de sabonetes | 50,00 | 03/11/2026 |
| 2 | Maria | 104 | Pedido de cadernos | 35,50 | 05/11/2026 |
| 3 | João | NULL | NULL | NULL | NULL |

### 2. Somente clientes com pedidos (INNER JOIN)

```sql
SELECT c.id_cliente, c.nome, p.id_pedido, p.descricao, p.valor, p.data_pedido
FROM clientes c
INNER JOIN pedidos p ON p.id_cliente = c.id_cliente
ORDER BY c.id_cliente, p.id_pedido;
```

Retorna Ana e Maria. João some, pois não tem pedido.

### 3. Somente clientes sem pedidos (LEFT JOIN + IS NULL)

```sql
SELECT c.id_cliente, c.nome
FROM clientes c
LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
WHERE p.id_pedido IS NULL;
```

| ID_CLIENTE | NOME |
|---|---|
| 3 | João |

> Use no `WHERE` uma coluna que nunca é `NULL` na tabela da direita (a PK, `id_pedido`). Assim um pedido real com valor nulo não é confundido com "sem pedido".

## Resumo

| Consulta | Quem aparece |
|---|---|
| LEFT JOIN | Ana, Maria e João (João com `NULL`) |
| INNER JOIN | Ana e Maria |
| LEFT JOIN + `IS NULL` | Só João |

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
