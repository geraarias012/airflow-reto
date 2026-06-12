import pandas as pd


def aplicar_reglas():

    ruta = "/opt/airflow/data/devoluciones_validacion.csv"

    df = pd.read_csv(ruta)

    estados = []
    reglas = []

    for _, fila in df.iterrows():

        # Si la validación falló, no aplicar reglas
        if fila["validacion"] != "OK":
            estados.append("ERROR")
            reglas.append("Registro inválido")
            continue

        monto = fila["monto"]

        if monto <= 1000:
            estados.append("APROBADA")
            reglas.append("Aprobación automática")

        elif monto <= 5000:
            estados.append("PENDIENTE")
            reglas.append("Requiere aprobación del gerente")

        else:
            estados.append("REVISION")
            reglas.append("Revisión especial")

    df["estado"] = estados
    df["regla_aplicada"] = reglas

    print("RESULTADO DE LAS REGLAS")

    print(df[[
        "transaction_id",
        "monto",
        "estado",
        "regla_aplicada"
    ]])

    df.to_csv("/opt/airflow/data/devoluciones_procesadas.csv", index=False)