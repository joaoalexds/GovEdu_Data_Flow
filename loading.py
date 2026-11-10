import os
import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv


def create_conn():
    load_dotenv()
    string_url = URL.create(
        "mysql+pymysql",
        username=os.getenv('db_user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        database=os.getenv('database'),
        port=int(os.getenv('port'))
    )
    engine = create_engine(string_url)
    return engine

def loading(df: pd.DataFrame, engine):
    try:
        df.to_sql(
            name= 'gastos_ensino_superior',
            con= engine,
            if_exists= 'append',
            index= False,
            chunksize= 1000,
        )
        linhas = df.shape[0]
        print(f"Foram passadas a DB {linhas} linhas")
        return linhas
    except Exception as e:
        print(e)
