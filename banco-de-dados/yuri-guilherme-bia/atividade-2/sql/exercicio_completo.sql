-- =====================================================
-- exercicio_completo.sql  (tudo em um único arquivo)
-- =====================================================

CREATE TABLE clientes (
    id_cliente NUMBER PRIMARY KEY,
    nome       VARCHAR2(100) NOT NULL
);

CREATE TABLE pedidos (
    id_pedido   NUMBER PRIMARY KEY,
    id_cliente  NUMBER NOT NULL,
    descricao   VARCHAR2(200),
    valor       NUMBER(10,2),
    data_pedido DATE,
    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

INSERT INTO clientes (id_cliente, nome) VALUES (1, 'Ana');
INSERT INTO clientes (id_cliente, nome) VALUES (2, 'Maria');
INSERT INTO clientes (id_cliente, nome) VALUES (3, 'João');

INSERT INTO pedidos (id_pedido, id_cliente, descricao, valor, data_pedido)
VALUES (101, 1, 'Pedido de material', 150.00, DATE '2026-11-01');

INSERT INTO pedidos (id_pedido, id_cliente, descricao, valor, data_pedido)
VALUES (102, 1, 'Pedido de perfume', 80.00, DATE '2026-11-02');

INSERT INTO pedidos (id_pedido, id_cliente, descricao, valor, data_pedido)
VALUES (103, 2, 'Pedido de sabonetes', 50.00, DATE '2026-11-03');

INSERT INTO pedidos (id_pedido, id_cliente, descricao, valor, data_pedido)
VALUES (104, 2, 'Pedido de cadernos', 35.50, DATE '2026-11-05');

COMMIT;


-- (1) Todos os clientes com seus pedidos (LEFT JOIN)
SELECT c.id_cliente,
       c.nome,
       p.id_pedido,
       p.descricao,
       p.valor,
       p.data_pedido
FROM clientes c
LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
ORDER BY c.id_cliente, p.id_pedido;

-- (2) Somente clientes com pedidos (INNER JOIN)
SELECT c.id_cliente,
       c.nome,
       p.id_pedido,
       p.descricao,
       p.valor,
       p.data_pedido
FROM clientes c
INNER JOIN pedidos p ON p.id_cliente = c.id_cliente
ORDER BY c.id_cliente, p.id_pedido;

-- (3) Somente clientes sem pedidos (LEFT JOIN + IS NULL)
SELECT c.id_cliente,
       c.nome
FROM clientes c
LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
WHERE p.id_pedido IS NULL;
