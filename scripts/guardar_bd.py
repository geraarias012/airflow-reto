import pandas as pd
import sqlite3


def combinar_datos(ti):
    # Combina todos los datos para guardar en BD
    
    dataframes = []
    
    # 1. No aprobados por datos faltantes
    datos_dict = ti.xcom_pull(task_ids='validar_datos')
    df_no_aprobados = pd.read_json(datos_dict["no_aprobados"])
    dataframes.append(df_no_aprobados)
    
    # 2. Fraudes y aprobadas automáticas de reglas
    datos_reglas = ti.xcom_pull(task_ids='aplicar_reglas')
    df_fraudes = pd.read_json(datos_reglas["fraudes"])
    df_aprobadas_auto = pd.read_json(datos_reglas["aprobadas"])
    dataframes.append(df_fraudes)
    dataframes.append(df_aprobadas_auto)
    
    # 3. Aprobadas del gerente
    datos_gerente = ti.xcom_pull(task_ids='aprobacion_gerente')
    df_aprobadas_gerente = pd.read_json(datos_gerente["aprobadas_gerente"])
    dataframes.append(df_aprobadas_gerente)
    
    # 4. Aprobadas por validación de tiempo
    datos_tiempo = ti.xcom_pull(task_ids='validar_tiempo')
    df_aprobadas_tiempo = pd.read_json(datos_tiempo["aprobadas_tiempo"])
    dataframes.append(df_aprobadas_tiempo)
    
    # 5. Pendientes de tiempo (aún sin aprobar)
    df_pendientes_tiempo = pd.read_json(datos_tiempo["pendientes_tiempo"])
    dataframes.append(df_pendientes_tiempo)
    
    # Combinar todos sin resetear índice, ordenar por transaction_id
    df_combinado = pd.concat(dataframes, ignore_index=False)
    df_combinado = df_combinado.sort_values('transaction_id')
    
    print(f"Total de registros a guardar: {len(df_combinado)}")
    
    return df_combinado.to_json()


def guardar_bd(ti):

    datos = ti.xcom_pull(task_ids='combinar_datos')

    ruta_bd = "/opt/airflow/database/devoluciones.db"

    # Leer JSON
    df = pd.read_json(datos)

    # Convertir fecha de string a datetime para la base de datos
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Conectar a SQLite
    conexion = sqlite3.connect(ruta_bd)

    # Guardar la tabla
    df.to_sql(
        "devoluciones",
        conexion,
        if_exists="replace",
        index=False
    )

    conexion.commit()

    total = conexion.execute(
        "SELECT COUNT(*) FROM devoluciones"
    ).fetchone()[0]

    print("BASE DE DATOS ACTUALIZADA")
    print("")
    print(f"Registros guardados: {total}")

    conexion.close()