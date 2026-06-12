from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

from validar import validar_datos
from leer_csv import leer_csv
from reglas import aplicar_reglas
from guardar_bd import guardar_bd
from reportes import reporte_diario, reporte_semanal

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
    guardar = PythonOperator(
        task_id="guardar_bd",
        python_callable=guardar_bd,
    )
    reporte_diario = PythonOperator(
        task_id="reporte_diario",
        python_callable=reporte_diario,
    )
    reporte_semanal = PythonOperator(
        task_id="reporte_semanal",
        python_callable=reporte_semanal,
    )

    leer_archivo >> validar_archivo >> reglas >> guardar >> reporte_diario >> reporte_semanal
