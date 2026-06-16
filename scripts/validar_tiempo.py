import pandas as pd
from datetime import datetime, timedelta


def validar_tiempo(ti):

    datos_dict = ti.xcom_pull(task_ids='aprobacion_gerente')
    
    # Extraer pendientes de tiempo
    datos = datos_dict["pendientes_tiempo"]
    df = pd.read_json(datos)
    
    # Convertir fecha a datetime
    df["fecha"] = pd.to_datetime(df["fecha"])
    
    # Fecha actual
    fecha_actual = datetime.now()
    tiempo_minimo = timedelta(days=1)
    
    aprobadas_tiempo = []
    pendientes_tiempo = []
    
    for idx, fila in df.iterrows():
        fecha_devolucion = fila["fecha"]
        dias_transcurridos = fecha_actual - fecha_devolucion
        
        if dias_transcurridos >= tiempo_minimo:
            # Han pasado al menos 1 día: aprobadas
            df.loc[idx, "estado"] = "APROBADA"
            aprobadas_tiempo.append(idx)
        else:
            # Aún no ha pasado 1 día: siguen pendientes
            df.loc[idx, "estado"] = "PENDIENTE"
            pendientes_tiempo.append(idx)
    
    print("VALIDACIÓN DE TIEMPO")
    print(df.head())
    
    # Convertir fecha a string para mantener formato original
    df["fecha"] = df["fecha"].astype(str)
    
    # Retornar dos grupos
    aprobadas = df[df["estado"] == "APROBADA"].to_json()
    pendientes = df[(df["estado"] == "PENDIENTE") & (df.index.isin(pendientes_tiempo))].to_json()
    
    return {
        "aprobadas_tiempo": aprobadas,
        "pendientes_tiempo": pendientes
    }
