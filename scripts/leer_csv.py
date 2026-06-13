import pandas as pd


def leer_csv():

    ruta = "/opt/airflow/data/devoluciones.csv"

    df = pd.read_csv(ruta)

    print("Archivo leído correctamente")
    print(df.head())

    # retornamos el df para el siguiente paso
    return df.to_json()