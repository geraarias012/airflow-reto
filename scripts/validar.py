import pandas as pd

def validar_datos(ti):

    datos = ti.xcom_pull(task_ids='leer_csv')

    df = pd.read_json(datos)

    errores = []


    for _, fila in df.iterrows():

        error = []

        #Transacción ID
        if pd.isnull(fila['transaction_id']):
            error.append("Transacción ID es nulo")
        
        #Fecha de Devolución
        try:
            pd.to_datetime(fila['fecha'])
        except:
            error.append("Fecha no es una fecha válida")

        # Cuenta
        if pd.isna(fila["cuenta"]):
            error.append("cuenta vacía")

        # Monto
        if fila["monto"] <= 0 or pd.isna(fila["monto"]):
            error.append("monto inválido")

        # Moneda
        if pd.isna(fila["moneda"]):
            error.append("moneda vacía")

        errores.append(", ".join(error) if error else "OK")

    df["validacion"] = errores

    print(df)

    return df.to_json()