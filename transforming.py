import pandas as pd

def transforming(df: pd.DataFrame):
    #convertendo string -> float
    for i in ["valor_empenhado", "valor_liquidado", "valor_pago", "valor_restos_a_pagar_cancelado", "valor_restos_a_pagar_pagos"]:
        df[i] = (df[i]
                .str.replace(',', '.')
                .str.strip()
                )
        df[i] = df[i].astype(float)
        
    #criando as colunas numericas que queremos
    df['valor_abatido'] = df['valor_pago'] + df['valor_liquidado'] + df['valor_restos_a_pagar_cancelado']
    df['restos_a_pagar'] = df['valor_empenhado'] - df['valor_abatido']
    
    #retirando colunas que não usaremos mais
    df = df.drop(columns=['valor_liquidado', 'valor_pago', 'valor_restos_a_pagar_cancelado', 'valor_restos_a_pagar_pagos'])
    
    #agrupando gerando o df final
    df = df.groupby(["ano_mes","codigo_orgao_subordinado", "nome_orgao_subordinado", "nome_unidade_gestora", "nome_unidade_orcamentaria",
            "nome_orgao_superior", "nome_programa_orcamentario", "nome_acao", "nome_subtitulo", "descricao_complementar_localizador",
            "nome_categoria_economica", "nome_grupo_de_despesa"]
        )[['valor_empenhado', 'valor_abatido', 'restos_a_pagar']].sum().sort_values(by= 'nome_orgao_subordinado').reset_index()
    
    return df
