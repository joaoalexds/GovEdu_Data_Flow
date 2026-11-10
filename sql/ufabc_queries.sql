-- Quais foram todos os registros da UFABC?
SELECT * FROM gastos_ensino_superior WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC';

-- Quanto a UFABC empenhou e pagou por mês? Quanto falta para a UFABC pagar (acomulativo)
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

-- Quantos registros (gastos) a UFABC faz por mês e quanto esses gastos representam em valor empenhado?
SELECT
    ano_mes as mes,
    nome_orgao_subordinado as universidade,
    COUNT(nome_orgao_subordinado) as vezes,
    SUM(valor_empenhado) as valor_empenhado
FROM gastos_governo_db.gastos_ensino_superior
WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
GROUP BY ano_mes
ORDER BY mes ASC;

-- Qual foi o programa orcamentario mais associados aos registros da UFABC? E qual o valor empenhado no programa?
SELECT
    nome_programa_orcamentario as programa,
    COUNT(nome_programa_orcamentario) as quantas_vezes,
    SUM(valor_empenhado) as total_empenhado
FROM gastos_governo_db.gastos_ensino_superior
WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
GROUP BY nome_programa_orcamentario
ORDER BY quantas_vezes ASC;

-- Qual categoria economica estão mais presentes nos registros da UFABC? E qual o valor empenhado por categoria economica?
-- (relacionando a um grupo de despesa)
SELECT
    nome_categoria_economica as categoria_economica,
    nome_grupo_de_despesa as grupo_de_despesa,
    COUNT(nome_grupo_de_despesa) as quantas_vezes,
    SUM(valor_empenhado) as total_empenhado
FROM gastos_governo_db.gastos_ensino_superior
WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
GROUP BY nome_categoria_economica, nome_grupo_de_despesa
ORDER BY quantas_vezes DESC;

