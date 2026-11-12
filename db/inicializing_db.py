import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import ProgrammingError, OperationalError

def ler_arquivosql(caminho_arquivo):
    #lemos o arquivo sql
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        sql_completo = file.read()
        
    #lista todos os comandos
    comandos = []
    for comando in sql_completo.split(";"):
        #limpamos os comandos com strip
        comando_limpo = comando.strip()
        #usamos o if para checar se ele não ficou vazio
        if comando_limpo:
            comandos.append(comando_limpo)
    return comandos

def inicializing_db(comandos):
    load_dotenv()
    
    #criamos a url sem a db citada nela
    url_base = URL.create(
        "mysql+pymysql",
        username=os.getenv('db_user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=int(os.getenv('port'))
    )
    #cria a primeira url sem a Db nela
    #o autocommit pega o comando e o executa sem a necessidade de confirmacao, usado para executar comandos de alto nivel
    engine_base = create_engine(url_base, isolation_level='AUTOCOMMIT')
    
    #pega o comando que contenha a funcao create database e o executa
    #usamos o connect para retirar a "cautela" do sqlalchemy para o auto commit poder funcionar
    with engine_base.connect() as conn:
        for comando in comandos:
            if "CREATE DATABASE" in comando:
                conn.execute(text(comando))
                comandos.remove(comando)
                break
            
    #como já criamos a db agora podemos fazer a engine correta com a database
    url_final = url_base.set(database=os.getenv('database'))
    engine_final = create_engine(
        url_final,
        isolation_level='AUTOCOMMIT', #roda cada pedaco do codigo imediatamente
        pool_pre_ping=True, #testa a engine
        pool_recycle=280 #faz a manutencao da conexao antes dela encerrar
    )
    
    #vamos executar todos os outros comandos agora
    with engine_final.begin() as conn:
        for comando in comandos:
            try:
                conn.execute(text(comando))
            except(ProgrammingError, OperationalError) as error: #no caso de serem criados dois indeces add index cai nesse except
                if hasattr(error, 'orig') and error.orig.args[0] == 1061:
                    print(f"Aviso: Índice já existe")
    
    return engine_final