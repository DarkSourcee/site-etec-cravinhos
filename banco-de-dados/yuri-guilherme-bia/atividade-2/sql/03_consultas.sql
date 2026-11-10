-- =====================================================
-- 03_consultas.sql
-- As três consultas do exercício
-- =====================================================
ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';

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
