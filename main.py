#o main deve fazer a ingestão de arquivos e mudar os arquivos de pasta
#criar lista de arquivos não processados
import glob
import os
import shutil

from extraction import extraction
from transforming import transforming
from loading import create_conn, loading

arquivos = glob.glob('raw_data/*.csv')
linhas = 0

#montar um loop que percorre os arquivos e manda pra dentro das funções
for caminho_arquivo in arquivos:
    try:
        #1. extrair com def extraction, retorna um df completo
        df = extraction(caminho_arquivo)
        
        #2. transformar com def transforming (convertes tipos, exluir linhas e agrupar gastos iguais)
        df = transforming(df)
        
        #3. carregar na base de dados. (sql alchemy)
        #antes vamos criar a engine
        engine = create_conn()
        
        #com o parametro criado, chamamos a loading
        #chamamos o loading e aproveitamos para somar o total de linhas passadas a DB
        linhas += loading(df, engine)
        
        #mudar o arquivo de pasta
        #pegamos o nome do arquivo e geramos o destino do arquivo
        nome_arquivo = os.path.basename(caminho_arquivo)
        destino_arquivo = os.path.join('processed_data', nome_arquivo)
        
        #movemos com shutil (onde está -> para onde vai)
        shutil.move(caminho_arquivo, destino_arquivo)
    except:
        #apontar qual o arquivo que não subiu direito e mante-lo na mesma pasta
        print(f"O arquivo {os.path.basename(caminho_arquivo)}, apresentou erro ao ser carregado")

#gerando uma visualização organizada no terminal
print(f"{'-'*50}")
print("O processo foi concluido!")
print(f"Foram passadas um total de {linhas} linhas a DB")