-- query para ver os top 5 os que mais empenharam valor
SELECT 
    nome_orgao_subordinado AS universidade,
    SUM(valor_empenhado) AS total_gasto,
    SUM (valor_abatido) AS total_pago
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY total_gasto DESC
LIMIT 10;

-- criando um percentual de quanto cada universidade representa no total
SELECT
    nome_orgao_subordinado AS universidade,
    SUM(valor_empenhado) AS total_gasto,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 3
    ) AS porcentagem
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY total_gasto DESC
LIMIT 10;

-- criando uma contagem de quantas vezes cada universidade gastou e quanto elas representam do total da verba
SELECT
    nome_orgao_subordinado as universidade,
    COUNT(nome_orgao_subordinado) as quantos_gastos_teve,
    SUM(valor_empenhado) as valor_gasto,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 2
    ) AS percentual_por_programa
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY quantos_gastos_teve DESC
LIMIT 10;

-- somando o nome do programa orcamentario que mais gastou e quantas vezes ele gastou
SELECT
    nome_programa_orcamentario as programa_orcamentario,
    COUNT(nome_programa_orcamentario) as vezes_por_programa,
    SUM(valor_empenhado) as valor_por_programa,
    ROUND(
        ((SUM(valor_empenhado)) / (SELECT SUM(valor_empenhado) FROM gastos_governo_db.gastos_ensino_superior)) * 100, 2
    ) AS percentual_por_programa
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_programa_orcamentario
ORDER BY valor_por_programa DESC
LIMIT 10;

-- montante empenhado, pago e resto a pagar por categoria economica
SELECT
    nome_grupo_de_despesa as nome_categoria,
    SUM(valor_empenhado) as valor_empenhado, 
    SUM(valor_abatido) as valor_pago,
    SUM(restos_a_pagar) as restos
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY(nome_grupo_de_despesa)
ORDER BY nome_grupo_de_despesa ASC
LIMIT 10;
