import pandas as pd
import sqlite3


def generar_reportes():
    """Genera reportes diario y semanal en una sola función"""

    conexion = sqlite3.connect("/opt/airflow/database/devoluciones.db")

    df = pd.read_sql("SELECT * FROM devoluciones", conexion)

    # Reporte Diario
    reporte_diario = (
        df.groupby("fecha")
        .agg(
            total_devoluciones=("transaction_id", "count"),
            monto_aprobado=("monto", lambda x: x[df.loc[x.index, "estado"] == "APROBADA"].sum()),
            monto_pendiente=("monto", lambda x: x[df.loc[x.index, "estado"] == "PENDIENTE"].sum()),
            monto_no_aprobado=("monto", lambda x: x[(df.loc[x.index, "estado"] == "NO APROBADA POR DATOS FALTANTES") | (df.loc[x.index, "estado"] == "NO APROBADO POR POSIBLE FRAUDE")].sum()),
            aprobadas=("estado", lambda x: (x == "APROBADA").sum()),
            no_aprobadas=("estado", lambda x: (x == "NO APROBADA POR DATOS FALTANTES").sum()),
            fraude=("estado", lambda x: (x == "NO APROBADO POR POSIBLE FRAUDE").sum()),
            pendientes=("estado", lambda x: (x == "PENDIENTE").sum()),
        )
        .reset_index()
    )

    # Convertir fecha a formato dd-mm-yyyy
    reporte_diario["fecha"] = pd.to_datetime(reporte_diario["fecha"]).dt.strftime("%d-%m-%Y")

    reporte_diario.to_csv(
        "/opt/airflow/reports/reporte_diario.csv",
        index=False
    )

    print("\nREPORTE DIARIO")
    print(reporte_diario)

    # Reporte Semanal
    df["fecha"] = pd.to_datetime(df["fecha"])

    reporte_semanal = (
        df.groupby(
            pd.Grouper(key="fecha", freq="W")
        )
        .agg(
            total_devoluciones=("transaction_id", "count"),
            monto_aprobado=("monto", lambda x: x[df.loc[x.index, "estado"] == "APROBADA"].sum()),
            monto_pendiente=("monto", lambda x: x[df.loc[x.index, "estado"] == "PENDIENTE"].sum()),
            monto_no_aprobado=("monto", lambda x: x[(df.loc[x.index, "estado"] == "NO APROBADA POR DATOS FALTANTES") | (df.loc[x.index, "estado"] == "NO APROBADO POR POSIBLE FRAUDE")].sum()),
            aprobadas=("estado", lambda x: (x == "APROBADA").sum()),
            no_aprobadas=("estado", lambda x: (x == "NO APROBADA POR DATOS FALTANTES").sum()),
            fraude=("estado", lambda x: (x == "NO APROBADO POR POSIBLE FRAUDE").sum()),
            pendientes=("estado", lambda x: (x == "PENDIENTE").sum()),
        )
        .reset_index()
    )

    reporte_semanal["fecha_inicio"] = reporte_semanal["fecha"] - pd.Timedelta(days=6)
    reporte_semanal["fecha_fin"] = reporte_semanal["fecha"]

    reporte_semanal = reporte_semanal[[
        "fecha_inicio",
        "fecha_fin",
        "total_devoluciones",
        "monto_aprobado",
        "monto_pendiente",
        "monto_no_aprobado",
        "aprobadas",
        "no_aprobadas",
        "fraude",
        "pendientes"
    ]]

    # Convertir fechas a formato dd-mm-yyyy
    reporte_semanal["fecha_inicio"] = reporte_semanal["fecha_inicio"].dt.strftime("%d-%m-%Y")
    reporte_semanal["fecha_fin"] = reporte_semanal["fecha_fin"].dt.strftime("%d-%m-%Y")

    reporte_semanal.to_csv(
        "/opt/airflow/reports/reporte_semanal.csv",
        index=False
    )

    print("\nREPORTE SEMANAL")
    print(reporte_semanal)

    conexion.close()