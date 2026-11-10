-- =====================================================
-- 02_inserir_dados.sql
-- 3 clientes e 4 pedidos
-- João (id 3) fica sem pedido de propósito
-- =====================================================
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
