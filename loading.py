import pandas as pd

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
