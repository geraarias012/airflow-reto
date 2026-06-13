import pandas as pd
import sqlite3


def reporte_diario():

    conexion = sqlite3.connect("/opt/airflow/database/devoluciones.db")

    df = pd.read_sql("SELECT * FROM devoluciones", conexion)

    reporte = (
        df.groupby("fecha")
        .agg(
            total_devoluciones=("transaction_id", "count"),
            monto_total=("monto", "sum"),
            aprobadas=("estado", lambda x: (x == "APROBADA").sum()),
            pendientes=("estado", lambda x: (x == "PENDIENTE").sum()),
            revision=("estado", lambda x: (x == "REVISION").sum()),
            fraude=("estado", lambda x: (x == "POSIBLE FRAUDE").sum()),
            validaciones_fallidas=("validacion", lambda x: (x != "OK").sum())
        )
        .reset_index()
    )

    reporte.to_csv(
        "/opt/airflow/reports/reporte_diario.csv",
        index=False
    )

    print("\nREPORTE DIARIO")
    print(reporte)

    conexion.close()


def reporte_semanal():

    conexion = sqlite3.connect("/opt/airflow/database/devoluciones.db")

    df = pd.read_sql("SELECT * FROM devoluciones", conexion)

    df["fecha"] = pd.to_datetime(df["fecha"])

    reporte = (
        df.groupby(
            pd.Grouper(key="fecha", freq="W")
        )
        .agg(
            total_devoluciones=("transaction_id", "count"),
            monto_total=("monto", "sum"),
            aprobadas=("estado", lambda x: (x == "APROBADA").sum()),
            pendientes=("estado", lambda x: (x == "PENDIENTE").sum()),
            revision=("estado", lambda x: (x == "REVISION").sum()),
            fraude=("estado", lambda x: (x == "POSIBLE FRAUDE").sum()),
            validaciones_fallidas=("validacion", lambda x: (x != "OK").sum())
        )
        .reset_index()
    )

    reporte["fecha_inicio"] = reporte["fecha"] - pd.Timedelta(days=6)
    reporte["fecha_fin"] = reporte["fecha"]

    reporte = reporte[[
        "fecha_inicio",
        "fecha_fin",
        "total_devoluciones",
        "monto_total",
        "aprobadas",
        "pendientes",
        "revision",
        "fraude",
        "validaciones_fallidas"
    ]]

    reporte.to_csv(
        "/opt/airflow/reports/reporte_semanal.csv",
        index=False
    )

    print("\nREPORTE SEMANAL")
    print(reporte)

    conexion.close()