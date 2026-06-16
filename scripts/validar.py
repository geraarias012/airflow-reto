import pandas as pd

def validar_datos(ti):

    datos = ti.xcom_pull(task_ids='leer_csv')

    df = pd.read_json(datos)

    estados = []

    for _, fila in df.iterrows():

        error = False

        #Transacción ID
        if pd.isnull(fila['transaction_id']):
            error = True
        
        #Fecha de Devolución
        try:
            pd.to_datetime(fila['fecha'])
        except:
            error = True

        # Cuenta
        if pd.isna(fila["cuenta"]):
            error = True

        # Monto
        if fila["monto"] <= 0 or pd.isna(fila["monto"]):
            error = True

        # Moneda
        if pd.isna(fila["moneda"]):
            error = True

        if pd.isna(fila["tipo"]):
            error = True

        if error:
            estados.append("NO APROBADA POR DATOS FALTANTES")
        else:
            estados.append("PENDIENTE")

    df["estado"] = estados

    print(df)

    # Separar en dos grupos
    pendientes = df[df["estado"] == "PENDIENTE"].to_json()
    no_aprobados = df[df["estado"] == "NO APROBADA POR DATOS FALTANTES"].to_json()

    return {
        "pendientes": pendientes, 
        "no_aprobados": no_aprobados
    }