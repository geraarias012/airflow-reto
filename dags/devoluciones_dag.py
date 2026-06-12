from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hola_mundo():
    print("¡Hola, mundo!")  

with DAG(
    dag_id="devoluciones_dag",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
) as dag:

    tarea = PythonOperator(
        task_id="hola_mundo",
        python_callable=hola_mundo
    )   