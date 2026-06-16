import pandas as pd


def aplicar_reglas(ti):

    datos_dict = ti.xcom_pull(task_ids='validar_datos')

    # Extraer solo los pendientes
    datos = datos_dict["pendientes"]

    df = pd.read_json(datos)

    # Convertir fecha a datetime y agregar semana
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["semana"] = df["fecha"].dt.to_period("W")

    # Detectar fraude 
    conteo = (
        df.groupby(["cuenta", "semana"])
        .size()
        .reset_index(name="total")
    )
    cuentas_posible_fraude = conteo[conteo["total"] >= 3]

    # Marcar fraudes
    for _, fila in cuentas_posible_fraude.iterrows():
        mascara = (
            (df["cuenta"] == fila["cuenta"]) &
            (df["semana"] == fila["semana"])
        )
        df.loc[mascara, "estado"] = "NO APROBADO POR POSIBLE FRAUDE"

    # Aplicar reglas a registros que no son fraude
    df_no_fraude = df[df["estado"] != "NO APROBADO POR POSIBLE FRAUDE"].copy()
    
    # Separar en dos grupos
    aprobadas_auto = []
    para_gerente = []
    
    for idx, fila in df_no_fraude.iterrows():
        monto = fila["monto"]
        
        if monto <= 5000:
            # Aprobación automática
            df.loc[idx, "estado"] = "APROBADA"
            aprobadas_auto.append(idx)
        else:
            # Requiere aprobación del gerente
            df.loc[idx, "estado"] = "PENDIENTE"
            para_gerente.append(idx)

    df.drop(columns=["semana"], inplace=True)

    print("RESULTADO DE LAS REGLAS")
    print(df.head())

    # Retornar tres grupos
    fraudes = df[df["estado"] == "NO APROBADO POR POSIBLE FRAUDE"].to_json()
    aprobadas = df[df["estado"] == "APROBADA"].to_json()
    pendientes_gerente = df[(df["estado"] == "PENDIENTE") & (df.index.isin(para_gerente))].to_json()

    return {
        "fraudes": fraudes,
        "aprobadas": aprobadas,
        "pendientes_gerente": pendientes_gerente
    }