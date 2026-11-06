-- cria uma visualizacao de quanto a UFABC gastou e ainda deve pagar, mas acumulando e abatendo valor
SELECT 
    ano_mes as mes,
    nome_orgao_subordinado as universidade,
    SUM(valor_empenhado) as total_empenhado,
    SUM(valor_abatido) as valor_pago,
    SUM(SUM(valor_empenhado) - SUM(valor_abatido)) OVER (ORDER BY ano_mes ASC) AS falta_pagar_acumulado
FROM gastos_governo_db.gastos_ensino_superior
WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
GROUP BY ano_mes
ORDER BY mes ASC;

--vamos criar uma visualização de quantas vezes a UFABC fez algum gasto
--colocando um valor empenhado por mes
SELECT
    ano_mes as mes,
    nome_orgao_subordinado as universidade,
    COUNT(nome_orgao_subordinado) as vezes,
    SUM(valor_empenhado) as valor_empenhado
FROM gastos_governo_db.gastos_ensino_superior
WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
GROUP BY ano_mes
ORDER BY mes ASC;
