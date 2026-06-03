import pandas as pd
import joblib

modelo = joblib.load("models/modelo.pkl")
encoders = joblib.load("models/encoders.pkl")


def predecir_paciente(datos):

    df = pd.DataFrame([datos])

    # SEXO (seguro)
    df["sexo"] = encoders["sexo"].transform(df["sexo"])

    # SINTOMA (NO transformar si no existe)
    if df["sintoma"].iloc[0] in encoders["sintoma"].classes_:
        df["sintoma"] = encoders["sintoma"].transform(df["sintoma"])
    else:
        # fallback: usar el más común del dataset original
        df["sintoma"] = encoders["sintoma"].transform(
            [encoders["sintoma"].classes_[0]]
        )

    # CONDICION CRONICA
    if df["condicion_cronica"].iloc[0] in encoders["condicion_cronica"].classes_:
        df["condicion_cronica"] = encoders["condicion_cronica"].transform(
            df["condicion_cronica"]
        )
    else:
        df["condicion_cronica"] = encoders["condicion_cronica"].transform(
            [encoders["condicion_cronica"].classes_[0]]
        )

    pred = modelo.predict(df)

    prioridad = encoders["prioridad"].inverse_transform(pred)

    return prioridad[0]