import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

def grafico_maiores_valores_empenhado(engine):
    """
    Gera uma visualizacao das cinco faculdades que mais empenharam valor, 
    acompanhado de seu total_pago e restos a pagar
    """
    
    #cria a figura e o eixo
    fig, ax = plt.subplots(figsize=(16,10))
    
    
    #escrevemos a query que vai gerar nosso df
    query = """
    SELECT
        nome_orgao_subordinado AS Universidade,
        SUM(valor_empenhado) AS valor_empenhado,
        SUM(valor_abatido) AS valor_abatido,
        SUM(restos_a_pagar) AS restos_a_pagar
    FROM gastos_governo_db.gastos_ensino_superior
    GROUP BY nome_orgao_subordinado
    ORDER BY valor_empenhado DESC
    LIMIT 5;
    """
    
    #com os dados da query montamos nosso df e fechamos a conexao
    df = pd.read_sql(query, con=engine)
    
    #vamos usar o df melt para "alongar a tabela" assim a gente consegue "unir" os dados dos valores
    #em uma unica coluna chamada valor que vamos usar para o nosso eixo y, criamos a coluna tipo para ser cada barrinha
    df_melt = pd.melt(
        df, 
        id_vars= ['Universidade'], #variavel de identificacao, indica a coluna que não sera derretida
        value_vars= ['valor_empenhado', 'valor_abatido', 'restos_a_pagar'], #coluna com os valores numericos que vai ser fundida em uma unica coluna
        var_name= 'Tipo', #é o nome da coluna que armazena os nomes das colunas originais
        value_name= 'Valor'#é a coluna que vai guardar os valores
    )
    
    #vamos setar a paleta de cores que vamos usar
    paleta_cores = {
        'valor_empenhado' : "#64a7dd", #azul
        'restos_a_pagar' : "#ee0e0e", #vermelho
        'valor_abatido' : "#648aa8df"
    }
    
    #sns barplot para gerar o grafico
    sns.barplot(
        data=df_melt,
        x='Universidade', 
        y='Valor',
        hue='Tipo', #separa os elementos de uma mesma coluna, por esse valor adicional e os colore de maneira diferente
        palette=paleta_cores,
        zorder=2,
        ax=ax
    )
    
    #linhas de grade
    plt.grid(
        axis='y',          # Coloca grade apenas no eixo Y (linhas horizontais)
        color='gray',      # Cor da linha
        linestyle='--',    # Estilo tracejado
        linewidth=0.5,     # Espessura da linha
        alpha=0.7,         # Transparência
        zorder=1           # Joga a grade para trás das barras
    )
    
    #configurar a visualizacao
    ax.set_title("Valor empenhado vs Valor abatido vs Resto a pagar", fontsize= 14, pad= 15)
    ax.set_xlabel("Universidade", fontsize= 12)
    ax.set_ylabel('Valor (em milhões de R$)', fontsize= 12)
    
    #deixa os nomes do eixo x um pouco angulados para facilitar a leitura
    ax.tick_params(axis='x', rotation= 30)
    
    fig.tight_layout()
    plt.show()

def visualizacao_mes_mes_ufabc(engine):
    """
    Gera uma visualização do total empenhado, pago e o quanto falta pagar 
    """
    #cria a figura e o eixo
    fig, ax = plt.subplots(figsize=(12,6))
    
    #escrevemos a query que vai gerar nosso df
    #escrevemos a query que vai gerar nosso df
    query = """
    SELECT 
        ano_mes as mes,
        nome_orgao_subordinado as Universidade,
        SUM(valor_empenhado) as valor_empenhado,
        SUM(valor_abatido) as valor_abatido,
        SUM(SUM(valor_empenhado) - SUM(valor_abatido)) OVER (ORDER BY ano_mes ASC) AS restos_a_pagar
    FROM gastos_governo_db.gastos_ensino_superior
    WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
    GROUP BY ano_mes
    ORDER BY mes ASC;
    """
    
    #com os dados da query montamos nosso df e fechamos a conexao
    df = pd.read_sql(query, con=engine)
    
    df_melt = pd.melt(
        df, 
        id_vars= ['mes'], #variavel de identificacao, indica a coluna que não sera derretida
        value_vars= ['valor_empenhado', 'valor_abatido', 'restos_a_pagar'], #coluna com os valores numericos que vai ser fundida em uma unica coluna
        var_name= 'Tipo', #é o nome da coluna que armazena os nomes das colunas originais
        value_name= 'Valor'#é a coluna que vai guardar os valores
    )
    
    #vamos setar a paleta de cores que vamos usar
    paleta_cores = {
        'valor_empenhado' : "#64a7dd", #azul
        'restos_a_pagar' : "#ee0e0e", #vermelho
        'valor_abatido' : "#648aa8df"
    }
    
    #sns barplot para gerar o grafico
    sns.barplot(
        data=df_melt,
        x='mes', 
        y='Valor',
        hue='Tipo', #separa os elementos de uma mesma coluna, por esse valor adicional e os colore de maneira diferente
        palette=paleta_cores,
        zorder=2,
        ax=ax
    )
    
    #linhas de grade
    plt.grid(
        axis='y',          # Coloca grade apenas no eixo Y (linhas horizontais)
        color='gray',      # Cor da linha
        linestyle='--',    # Estilo tracejado
        linewidth=0.5,     # Espessura da linha
        alpha=0.7,         # Transparência
        zorder=1           # Joga a grade para trás das barras
    )
    
    #configurar a visualizacao
    ax.set_title("Valor empenhado vs Valor abatido vs Resto a pagar (UFABC)", fontsize= 14, pad= 15)
    ax.set_xlabel("Data", fontsize= 12)
    ax.set_ylabel('Valor (em milhões R$)', fontsize= 12)
    
    #deixa os nomes do eixo x um pouco angulados para facilitar a leitura
    ax.tick_params(axis='x', rotation= 30)
    
    fig.tight_layout()
    plt.show()

def registros_mensais_ufabc(engine):
    fig, ax = plt.subplots(figsize=(12,6))
    
    #escrevemos a query que vai gerar nosso df
    query = """
    SELECT
        ano_mes as mes,
        nome_orgao_subordinado as universidade,
        COUNT(nome_orgao_subordinado) as vezes
    FROM gastos_governo_db.gastos_ensino_superior
    WHERE nome_orgao_subordinado = 'Fundação Universidade Federal do ABC'
    GROUP BY ano_mes
    ORDER BY mes ASC;
    """
    
    #com os dados da query montamos nosso df e fechamos a conexao
    df = pd.read_sql(query, con=engine)
    
    df_melt = pd.melt(
        df, 
        id_vars= ['mes'], #variavel de identificacao, indica a coluna que não sera derretida
        value_vars= ['vezes'], #coluna com os valores numericos que vai ser fundida em uma unica coluna
        var_name= 'Tipo', #é o nome da coluna que armazena os nomes das colunas originais
        value_name= 'Valor'#é a coluna que vai guardar os valores
    )
    #vamos setar a paleta de cores que vamos usar
    paleta_cores = {
        'vezes' : "#64a7dd", #azul
    }
    
    #sns barplot para gerar o grafico
    sns.barplot(
        data=df_melt,
        x='mes', 
        y='Valor',
        hue='Tipo', #separa os elementos de uma mesma coluna, por esse valor adicional e os colore de maneira diferente
        palette=paleta_cores,
        zorder=2,
        ax=ax
    )
    
    #linhas de grade
    plt.grid(
        axis='y',          # Coloca grade apenas no eixo Y (linhas horizontais)
        color='gray',      # Cor da linha
        linestyle='--',    # Estilo tracejado
        linewidth=0.5,     # Espessura da linha
        alpha=0.7,         # Transparência
        zorder=1           # Joga a grade para trás das barras
    )
    
    #configurar a visualizacao
    ax.set_title("Quantidade de resgistros da UFABC", fontsize= 14, pad= 15)
    ax.set_xlabel("Data", fontsize= 12)
    ax.set_ylabel('Quantidade', fontsize= 12)
    
    #deixa os nomes do eixo x um pouco angulados para facilitar a leitura
    ax.tick_params(axis='x', rotation= 30)
    
    fig.tight_layout()
    plt.show()

#o arquivo tem que ficar limpo para que ao ser importado, rode perfeitamente