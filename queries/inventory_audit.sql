-- queries/inventory_audit.sql
-- Objetivo: Avaliar financeiramente o estoque atual e identificar distorções de excesso.

SELECT 
    sku,
    categoria,
    estoque_atual,
    estoque_seguranca,
    custo_unitario,
    -- Valor financeiro total parado hoje no galpão para este SKU
    (estoque_atual * custo_unitario) AS valor_estoque_atual,
    -- Diferença absoluta de peças acima do nível de segurança
    (estoque_atual - estoque_seguranca) AS excesso_pecas,
    -- Capital financeiro potencialmente "congelado" acima do necessário
    ((estoque_atual - estoque_seguranca) * custo_unitario) AS capital_imobilizado_excesso
FROM tb_estoque
ORDER BY valor_estoque_atual DESC;
