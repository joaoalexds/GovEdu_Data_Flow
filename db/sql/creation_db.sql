CREATE DATABASE IF NOT EXISTS gastos_governo_DB
CHARACTER SET utf8mb4 -- seta o encoding para que nn tenhamos letras quebradas 
COLLATE utf8mb4_unicode_ci;

USE gastos_governo_DB;

CREATE TABLE IF NOT EXISTS gastos_ensino_superior(
    id INT AUTO_INCREMENT PRIMARY KEY,

    ano_mes VARCHAR(7) NOT NULL,
    codigo_orgao_subordinado INT(10) NOT NULL,
    nome_orgao_subordinado VARCHAR(250) NOT NULL,
    nome_unidade_gestora VARCHAR(250),
    nome_unidade_orcamentaria VARCHAR(250),
    nome_orgao_superior VARCHAR(100),
    nome_programa_orcamentario VARCHAR(250),
    nome_acao VARCHAR(250),
    nome_subtitulo VARCHAR(250),
    descricao_complementar_localizador VARCHAR(20), 
    nome_categoria_economica VARCHAR(250),
    nome_grupo_de_despesa VARCHAR(250),

    valor_empenhado DECIMAL(20, 2) DEFAULT 0.00,
    valor_abatido DECIMAL(20, 2) DEFAULT 0.00,
    restos_a_pagar DECIMAL(20, 2) DEFAULT 0.00
);

ALTER TABLE gastos_ensino_superior ADD INDEX idx_data(ano_mes);
ALTER TABLE gastos_ensino_superior ADD INDEX idx_codigo_subordinado(codigo_orgao_subordinado);
ALTER TABLE gastos_ensino_superior ADD INDEX idx_nome_subordinado(nome_orgao_subordinado);
ALTER TABLE gastos_ensino_superior ADD INDEX idx_orgao_superior(nome_orgao_superior);
