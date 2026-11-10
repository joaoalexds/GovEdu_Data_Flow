-- Quais foram as 10 instituições que mais empenharam valor?
SELECT 
    nome_orgao_subordinado AS universidade,
    SUM(valor_empenhado) AS total_empenhado,
    SUM (valor_abatido) AS total_pago
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY total_empenhado DESC
LIMIT 10;

-- Quantos pontos percentuais cada instituição representa do total empenhado?
SELECT
    nome_orgao_subordinado AS universidade,
    SUM(valor_empenhado) AS total_empenhado,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 3
    ) AS porcentagem
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY porcentagem DESC
LIMIT 10;

-- Quais foram as 10 instituições que mais tiveram registros (gastos)?
SELECT
    nome_orgao_subordinado as universidade,
    COUNT(nome_orgao_subordinado) as quantos_gastos_teve,
    SUM(valor_empenhado) as valor_gasto,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 2
    ) AS percentual_por_universidade
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY quantos_gastos_teve DESC
LIMIT 10;

-- Quais foram os 10 programas orcamentario que mais foram associados a um registro? Associando a eles um total empenhado e sua porcentagem do total
SELECT
    nome_programa_orcamentario as programa_orcamentario,
    COUNT(nome_programa_orcamentario) as vezes_por_programa,
    SUM(valor_empenhado) as valor_por_programa,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 2
    ) AS percentual_por_programa
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_programa_orcamentario
ORDER BY vezes_por_programa DESC
LIMIT 10;

-- Qual foi o montante empenhado por cada grupo de despesa? E quanto cada um abateu de seus gastos? 
SELECT
    nome_grupo_de_despesa as nome_categoria,
    SUM(valor_empenhado) as valor_empenhado, 
    SUM(valor_abatido) as valor_pago
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY(nome_grupo_de_despesa)
ORDER BY nome_grupo_de_despesa ASC
LIMIT 10;

-- Quanto foi empenhado e pago em cada mês? E quanto falta pagar (considerando acomulativo)
SELECT
    ano_mes as mes,
    SUM(valor_empenhado) as total_empenhado,
    SUM(valor_abatido) as valor_pago,
    SUM(SUM(valor_empenhado) - SUM(valor_abatido)) OVER (ORDER BY ano_mes ASC) AS falta_pagar_acumulado
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY(ano_mes)
ORDER BY(mes) ASC
LIMIT 12;