import pandas as pd


def leer_csv():

    ruta = "/opt/airflow/data/devoluciones.csv"

    df = pd.read_csv(ruta)

    print("Archivo leído correctamente")
    print(df.head())

    # Guardamos temporalmente para el siguiente paso
    df.to_csv("/opt/airflow/data/devoluciones_temp.csv", index=False)