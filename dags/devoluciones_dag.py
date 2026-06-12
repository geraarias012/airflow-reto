from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

from validar import validar_datos


def leer_csv():

    ruta = "/opt/airflow/data/devoluciones.csv"

    df = pd.read_csv(ruta)

    print("CSV leído correctamente")

    df = validar_datos(df)

    print(df)

    print("\nResumen de validaciones:")

    print(df["validacion"].value_counts())

with DAG(
    dag_id="devoluciones_dag",
    description="Lectura de archivo CSV de devoluciones",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["reto", "csv"],
) as dag:

    leer_archivo = PythonOperator(
        task_id="leer_csv",
        python_callable=leer_csv,
    )