-- queries/lead_time_analysis.sql
-- Objetivo: Auditar a eficiência e cumprimento de prazos contratuais por fornecedor.

SELECT 
    f.nome_fornecedor,
    f.regiao,
    COUNT(p.id_pedido) AS total_pedidos,
    -- Calcula a média de dias reais de entrega (Data Real - Data Pedido)
    AVG(julianday(p.data_entrega_real) - julianday(p.data_pedido)) AS lead_time_medio_real,
    -- Calcula a média de dias acordados em contrato (Data Prometida - Data Pedido)
    AVG(julianday(p.data_entrega_prometida) - julianday(p.data_pedido)) AS lead_time_acordado,
    -- Mede o desvio médio do contrato (valores positivos indicam atraso crônico)
    AVG(julianday(p.data_entrega_real) - julianday(p.data_entrega_prometida)) AS desvio_medio_prazo
FROM tb_pedidos_compra p
INNER JOIN tb_fornecedores f ON p.id_fornecedor = f.id_fornecedor
WHERE p.data_entrega_real IS NOT NULL
GROUP BY f.id_fornecedor, f.nome_fornecedor, f.regiao
ORDER BY lead_time_medio_real DESC;
