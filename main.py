#o main deve fazer a ingestão de arquivos e mudar os arquivos de pasta
#criar lista de arquivos não processados
import glob
import os
import shutil

from etl.extraction import extraction
from etl.transforming import transforming
from etl.loading import loading
from db.initializing_db import ler_arquivosql, inicializing_db
from grafics.grafics import grafico_maiores_valores_empenhado, visualizacao_mes_mes_ufabc, registros_mensais_ufabc

arquivos = glob.glob('data/raw_data/*.csv')
linhas = 0

#lemos o arquivo sql para que tenhamos os comandos necessarios
comandos = ler_arquivosql('db/sql/creation_db.sql')

#vamos comecar a executar os comandos sql com os comandos que obtivemos
#mandamos a engine final para engine
engine = inicializing_db(comandos)

#montar um loop que percorre os arquivos e manda pra dentro das funções
for caminho_arquivo in arquivos:
    try:
        #1. extrair com def extraction, retorna um df completo
        df = extraction(caminho_arquivo)
        
        #2. transformar com def transforming (convertes tipos, exluir linhas e agrupar gastos iguais)
        df = transforming(df)
        
        #com o parametro criado, chamamos a loading
        #chamamos o loading e aproveitamos para somar o total de linhas passadas a DB
        linhas += loading(df, engine)
        
        #mudar o arquivo de pasta
        #pegamos o nome do arquivo e geramos o destino do arquivo
        nome_arquivo = os.path.basename(caminho_arquivo)
        destino_arquivo = os.path.join('data/processed_data', nome_arquivo)
        
        #movemos com shutil (onde está -> para onde vai)
        shutil.move(caminho_arquivo, destino_arquivo)
    except:
        #apontar qual o arquivo que não subiu direito e mante-lo na mesma pasta
        print(f"O arquivo {os.path.basename(caminho_arquivo)}, apresentou erro ao ser carregado")

#gerando uma visualização organizada no terminal
print(f"{'-'*50}")
print("O processo foi concluido!")
print(f"Foram passadas um total de {linhas} linhas a DB")

#quero gerar as visualizações, queremos que liste as opcoes, o usuario digita a opcao, recebe o grafico e digita novamente as opcoes
print("-" * 50)
resp = input("Deseja visualizar os gráficos referentes à base de dados? (1 - Sim | 0 - Não): ")

if resp == '1':
    while True:
        print("-" * 50)
        print("Qual dos gráficos você deseja ver?")
        print("1 - Faculdades que mais empenharam valor")
        print("2 - Visualização dos gastos da UFABC mês a mês")
        print("3 - Quantos registros (compras) a UFABC")
        
        x = input("Digite o número do gráfico que deseja ver: ")
        
        if x == '1':
            grafico_maiores_valores_empenhado(engine)
        elif x == '2':
            visualizacao_mes_mes_ufabc(engine)
        elif x == '3':
            registros_mensais_ufabc(engine)
        else:
            print("Valor inválido. Tente novamente.")
            continue
            
        continuar = input("Deseja visualizar mais algum gráfico? (1 - Sim | 0 - Não): ")
        if continuar != '1':
            break