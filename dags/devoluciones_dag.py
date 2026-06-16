from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

from validar import validar_datos
from leer_csv import leer_csv
from reglas import aplicar_reglas
from aprobacion_gerente import aprobacion_gerente
from validar_tiempo import validar_tiempo
from guardar_bd import guardar_bd, get_no_aprobados, combinar_datos
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
    no_aprobados = PythonOperator(
        task_id="get_no_aprobados",
        python_callable=get_no_aprobados,
    )
    gerente = PythonOperator(
        task_id="aprobacion_gerente",
        python_callable=aprobacion_gerente,
    )
    tiempo = PythonOperator(
        task_id="validar_tiempo",
        python_callable=validar_tiempo,
    )
    combinar = PythonOperator(
        task_id="combinar_datos",
        python_callable=combinar_datos,
    )
    guardar = PythonOperator(
        task_id="guardar_bd",
        python_callable=guardar_bd,
    )
    reporte_diario_task = PythonOperator(
        task_id="reporte_diario",
        python_callable=reporte_diario,
    )
    reporte_semanal_task = PythonOperator(
        task_id="reporte_semanal",
        python_callable=reporte_semanal,
    )

    # Flujo con bifurcaciones
    leer_archivo >> validar_archivo
    
    # Bifurcación 1: no aprobados vs reglas
    validar_archivo >> [no_aprobados, reglas]
    
    # Bifurcación 2: reglas genera 3 outputs - fraudes y aprobadas van a guardar, pendientes a gerente
    reglas >> gerente
    
    # Bifurcación 3: gerente genera 2 outputs - aprobadas van a guardar, pendientes a validar tiempo
    gerente >> tiempo
    
    # Convergencia: todo confluye en combinar
    [no_aprobados, reglas, gerente, tiempo] >> combinar >> guardar >> [reporte_diario_task, reporte_semanal_task]

