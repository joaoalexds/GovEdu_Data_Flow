-- query para ver os top 5 os que mais empenharam 
SELECT 
    nome_orgao_subordinado AS universidade,
    SUM(valor_empenhado) AS total_gasto,
    SUM (valor_abatido) AS total_pago
FROM gastos_governo_db.gastos_ensino_superior
GROUP BY nome_orgao_subordinado
ORDER BY total_gasto DESC
LIMIT 10;

-- tentativa de criar um percentual de quanto cada universidade representa no total
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

