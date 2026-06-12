from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

from validar import validar_datos
from leer_csv import leer_csv
from reglas import aplicar_reglas

with DAG(
    dag_id="devoluciones_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    leer_archivo = PythonOperator(
        task_id="leer_csv",
        python_callable=leer_csv,
    )
    validar_archivo = PythonOperator(
        task_id="validar_datos",
        python_callable=validar_datos,
    )
    reglas = PythonOperator(
        task_id="aplicar_reglas",
        python_callable=aplicar_reglas,
    )   

    leer_archivo >> validar_archivo >> reglas
    