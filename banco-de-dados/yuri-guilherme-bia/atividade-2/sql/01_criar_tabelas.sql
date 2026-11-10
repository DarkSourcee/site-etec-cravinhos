-- =====================================================
-- 01_criar_tabelas.sql
-- Cria CLIENTES (lado 1) e PEDIDOS (lado N) com FK
-- Oracle SQL
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
