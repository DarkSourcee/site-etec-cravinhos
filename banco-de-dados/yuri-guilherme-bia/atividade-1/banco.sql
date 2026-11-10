-- Exercícios de CRUD — MySQL
CREATE DATABASE IF NOT EXISTS exercicios_crud CHARACTER SET utf8mb4;
USE exercicios_crud;

-- Exercício 1 — Alunos
CREATE TABLE IF NOT EXISTS alunos (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    curso VARCHAR(100) NOT NULL
);

-- Exercício 2 — Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    preco      DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL
);

-- Exercício 3 — Funcionários
CREATE TABLE IF NOT EXISTS funcionarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    cargo         VARCHAR(100) NOT NULL,
    salario       DECIMAL(10,2) NOT NULL,
    data_admissao DATE NOT NULL
);

-- Registros de teste (mínimo de 3 por tabela)
INSERT INTO alunos (nome, idade, curso) VALUES
    ('Ana Souza', 17, 'Informática'),
    ('Bruno Lima', 18, 'Administração'),
    ('Carla Mendes', 16, 'Informática');

INSERT INTO produtos (nome, preco, quantidade) VALUES
    ('Caderno 200 folhas', 18.90, 40),
    ('Caneta azul', 2.50, 3),
    ('Mochila escolar', 129.99, 4);

INSERT INTO funcionarios (nome, cargo, salario, data_admissao) VALUES
    ('Marcos Silva', 'Analista', 4200.00, '2021-03-15'),
    ('Fernanda Costa', 'Assistente', 2500.00, '2022-07-01'),
    ('Paulo Rocha', 'Analista', 3800.50, '2023-01-10');

-- ===== Consultas dos desafios extras (referência) =====
-- Alunos: pesquisar por nome
--   SELECT * FROM alunos WHERE nome LIKE '%Ana%';
-- Produtos: estoque baixo e valor total do estoque
--   SELECT * FROM produtos WHERE quantidade < 5;
--   SELECT SUM(preco * quantidade) AS total_estoque FROM produtos;
-- Funcionários: por cargo, salário > 3000 e média salarial
--   SELECT * FROM funcionarios WHERE cargo LIKE '%Analista%';
--   SELECT * FROM funcionarios WHERE salario > 3000;
--   SELECT AVG(salario) AS media_salarial FROM funcionarios;
