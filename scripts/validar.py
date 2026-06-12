import pandas as pd

def validar_datos(df):

    df = df.copy()

    errores = []

    # Validar que no haya valores nulos

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

        # Cuentas
        if pd.isna(fila["cuenta_origen"]):
            error.append("cuenta origen vacía")

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

    return df