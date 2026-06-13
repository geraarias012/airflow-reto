import pandas as pd
import sqlite3


def guardar_bd(ti):

    datos = ti.xcom_pull(task_ids='aplicar_reglas')

    ruta_bd = "/opt/airflow/database/devoluciones.db"

    # Leer JSON
    df = pd.read_json(datos)

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