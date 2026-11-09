from sqlalchemy import text

def criar_config_db(caminho_arquivo, engine):
    #le o arquivo sql que fizemos
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        sql_completo = file.read()
        
    #criando a lista pros comandos
    comandos = []
    #vamos pegar a leitura do arquivo e separar o pelo ;
    for comando in sql_completo.split(";"):
        #limpamos os comandos com strip
        comando_limpo = comando.strip
        #usamos o if para checar se ele não ficou vazio
        if comando_limpo:
            comandos.append(comando_limpo)
    for comando in comandos:
        engine.execute(text(comando))


