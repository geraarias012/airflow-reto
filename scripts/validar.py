import pandas as pd

def validar_datos():

    ruta = "/opt/airflow/data/devoluciones_temp.csv"

    df = pd.read_csv(ruta)

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
        if pd.isna(fila["cuenta_destino"]):
            error.append("cuenta destino vacía")

        # Monto
        if fila["monto"] <= 0:
            error.append("monto inválido")

        # Moneda
        if pd.isna(fila["moneda"]):
            error.append("moneda vacía")

        errores.append(", ".join(error) if error else "OK")

    df["validacion"] = errores

    print(df)

    df.to_csv("/opt/airflow/data/devoluciones_validacion.csv", index=False)