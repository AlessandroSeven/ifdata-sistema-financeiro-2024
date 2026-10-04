-- IFData: base individual, data-base 31/12/2024. Valores em R$ mil.
-- SegmentoTCB é um agrupamento analítico construído a partir do TCB,
-- não equivale aos segmentos regulatórios S1-S5.
DROP VIEW IF EXISTS vw_kpis;
DROP VIEW IF EXISTS vw_segmentos;
DROP VIEW IF EXISTS vw_top_ativos;
DROP VIEW IF EXISTS vw_top_lucro;
CREATE VIEW vw_kpis AS
SELECT DataBase,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(PatrimonioLiquido_R_mil) AS patrimonio_liquido_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil,
       SUM(CASE WHEN LucroLiquido_R_mil > 0 THEN 1 ELSE 0 END) AS instituicoes_com_lucro,
       SUM(CASE WHEN LucroLiquido_R_mil < 0 THEN 1 ELSE 0 END) AS instituicoes_com_prejuizo,
       1.0 * SUM(CarteiraCreditoClassificada_R_mil) / NULLIF(SUM(AtivoTotal_R_mil),0) AS carteira_sobre_ativo,
       1.0 * SUM(LucroLiquido_R_mil) / NULLIF(SUM(PatrimonioLiquido_R_mil),0) AS lucro_sobre_PL_final_proxy
FROM instituicoes GROUP BY DataBase;
CREATE VIEW vw_segmentos AS
SELECT DataBase, SegmentoTCB,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(PatrimonioLiquido_R_mil) AS patrimonio_liquido_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil
FROM instituicoes GROUP BY DataBase, SegmentoTCB;
CREATE VIEW vw_top_ativos AS
SELECT Instituicao, SegmentoTCB, AtivoTotal_R_mil, CarteiraCreditoClassificada_R_mil,
       PatrimonioLiquido_R_mil, LucroLiquido_R_mil
FROM instituicoes ORDER BY AtivoTotal_R_mil DESC LIMIT 10;
CREATE VIEW vw_top_lucro AS
SELECT Instituicao, SegmentoTCB, AtivoTotal_R_mil, PatrimonioLiquido_R_mil, LucroLiquido_R_mil
FROM instituicoes ORDER BY LucroLiquido_R_mil DESC LIMIT 10;

-- Consulta detalhada por filtros: edite os valores abaixo ou remova as condições.
SELECT SegmentoTCB, TCB, TipoControle, TI_Codigo,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil
FROM instituicoes
WHERE DataBase = '2024-12-31'
GROUP BY SegmentoTCB, TCB, TipoControle, TI_Codigo
ORDER BY ativo_total_R_mil DESC;
