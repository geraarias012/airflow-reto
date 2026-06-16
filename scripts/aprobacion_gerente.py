import pandas as pd


def aprobacion_gerente(ti):

    datos_dict = ti.xcom_pull(task_ids='aplicar_reglas')
    
    # Extraer pendientes del gerente
    datos = datos_dict["pendientes_gerente"]
    df = pd.read_json(datos)
    
    aprobadas_gerente = []
    para_validar_tiempo = []
    
    for idx, fila in df.iterrows():
        monto = fila["monto"]
        
        if monto <= 10000:
            # Entre 5000 y 10000: aprobadas
            df.loc[idx, "estado"] = "APROBADA"
            aprobadas_gerente.append(idx)
        else:
            # Mayor a 10000: requiere validación de tiempo
            df.loc[idx, "estado"] = "PENDIENTE"
            para_validar_tiempo.append(idx)
    
    print("APROBACIÓN GERENTE")
    print(df.head())
    
    # Convertir fecha a string para mantener formato original
    df["fecha"] = df["fecha"].astype(str)
    
    # Retornar dos grupos
    aprobadas = df[df["estado"] == "APROBADA"].to_json()
    pendientes_tiempo = df[(df["estado"] == "PENDIENTE") & (df.index.isin(para_validar_tiempo))].to_json()
    
    return {
        "aprobadas_gerente": aprobadas,
        "pendientes_tiempo": pendientes_tiempo
    }
