#nesse arquivo vamos extrair as informações que queremos, apenas

import pandas as pd

colunas_desejadas = [
    "Ano e mês do lançamento", "Nome Órgão Superior",
    "Código Órgão Subordinado", "Nome Órgão Subordinado", 
    "Nome Unidade Gestora", "Nome Unidade Orçamentária", 
    "Nome Programa Orçamentário", "Nome Ação", 
    "Nome Categoria Econômica", "Nome Grupo de Despesa",
    "Valor Liquidado (R$)", "Valor Pago (R$)",
    "Valor Restos a Pagar Cancelado (R$)", "Valor Restos a Pagar Pagos (R$)", 
    "Nome Subfunção", "Valor Empenhado (R$)", 
    "Nome Subtítulo", "Descrição Complementar Localizador",
    "Nome Subtítulo", "Descrição Complementar Localizador",
]

def extraction(file):
    df = pd.read_csv(file,
                sep=';',
                encoding='latin-1',
                usecols=colunas_desejadas)
    
    df = df.rename(columns={
    "Nome Subtítulo": "nome_subtitulo",
    "Descrição Complementar Localizador":"descricao_complementar_localizador",
    "Ano e mês do lançamento": "ano_mes",
    "Nome Órgão Superior": "nome_orgao_superior",
    "Código Órgão Subordinado": "codigo_orgao_subordinado",
    "Nome Órgão Subordinado": "nome_orgao_subordinado",
    "Nome Unidade Gestora": "nome_unidade_gestora",
    "Nome Unidade Orçamentária": "nome_unidade_orcamentaria",
    "Nome Programa Orçamentário": "nome_programa_orcamentario",
    "Nome Ação": "nome_acao",
    "Nome Categoria Econômica": "nome_categoria_economica",
    "Nome Grupo de Despesa": "nome_grupo_de_despesa",
    "Valor Liquidado (R$)": "valor_liquidado",
    "Valor Pago (R$)": "valor_pago",
    "Valor Restos a Pagar Cancelado (R$)": "valor_restos_a_pagar_cancelado",
    "Valor Restos a Pagar Pagos (R$)": "valor_restos_a_pagar_pagos",
    "Nome Subfunção": "nome_subfuncao",
    "Valor Empenhado (R$)": "valor_empenhado",
    "Nome Subtítulo": "nome_subtitulo",
    "Descrição Complementar Localizador": "descricao_complementar_localizador"
    })
    df = df[df['nome_subfuncao'] == 'Ensino superior']
    
    df = df.dropna()
    return df
