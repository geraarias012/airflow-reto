import pandas as pd


def aplicar_reglas(ti):

    datos = ti.xcom_pull(task_ids='validar_datos')

    df = pd.read_json(datos)

    estados = []
    reglas = []

    for _, fila in df.iterrows():

        # Si la validación falló, no aplicar reglas
        if fila["validacion"] != "OK":
            estados.append("ERROR")
            reglas.append("Registro invalido")
            continue

        monto = fila["monto"]

        if monto <= 1000:
            estados.append("APROBADA")
            reglas.append("Aprobación automatica")

        elif monto <= 5000:
            estados.append("PENDIENTE")
            reglas.append("Requiere aprobacion del gerente")

        else:
            estados.append("REVISION")
            reglas.append("Revisión especial")

    df["estado"] = estados
    df["regla_aplicada"] = reglas

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["semana"] = df["fecha"].dt.to_period("W")

    conteo = (
        df.groupby(["cuenta", "semana"])
        .size()
        .reset_index(name="total")
    )

    cuentas_posible_fraude = conteo[conteo["total"] >= 3]

    for _, fila in cuentas_posible_fraude.iterrows():

        mascara = (
            (df["cuenta"] == fila["cuenta"]) &
            (df["semana"] == fila["semana"])
        )

        df.loc[mascara, "estado"] = "POSIBLE FRAUDE"
        df.loc[mascara, "regla_aplicada"] = "Marcado como posible fraude por multiples devoluciones"

    df.drop(columns=["semana"], inplace=True)

    print("RESULTADO DE LAS REGLAS")

    print(df[[
        "transaction_id",
        "monto",
        "estado",
        "regla_aplicada"
    ]])

    return df.to_json()