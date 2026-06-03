import pandas as pd
import random

datos = []

sintomas_alta = [
    "dificultad respiratoria",
    "dolor toracico",
    "perdida de conciencia",
    "hemorragia",
    "convulsiones"
]

sintomas_media = [
    "fiebre",
    "fractura",
    "infeccion",
    "dolor abdominal",
    "tos persistente"
]

sintomas_baja = [
    "resfriado",
    "cefalea leve",
    "alergia",
    "control rutinario",
    "malestar general"
]

condiciones = [
    "ninguna",
    "diabetes",
    "hipertension",
    "asma",
    "diabetes e hipertension"
]

id_paciente = 1

# BAJA
for _ in range(166):
    datos.append([
        id_paciente,
        random.randint(5, 80),
        random.choice(["M", "F"]),
        round(random.uniform(36.0, 37.4), 1),
        random.randint(60, 90),
        random.randint(100, 130),
        random.randint(60, 85),
        random.randint(96, 100),
        random.randint(0, 3),
        random.choice(sintomas_baja),
        random.choice(condiciones),
        "BAJA"
    ])
    id_paciente += 1

# MEDIA
for _ in range(167):
    datos.append([
        id_paciente,
        random.randint(10, 90),
        random.choice(["M", "F"]),
        round(random.uniform(37.5, 39.0), 1),
        random.randint(90, 120),
        random.randint(120, 160),
        random.randint(75, 95),
        random.randint(90, 95),
        random.randint(4, 7),
        random.choice(sintomas_media),
        random.choice(condiciones),
        "MEDIA"
    ])
    id_paciente += 1

# ALTA
for _ in range(167):
    datos.append([
        id_paciente,
        random.randint(1, 95),
        random.choice(["M", "F"]),
        round(random.uniform(39.0, 41.0), 1),
        random.randint(120, 160),
        random.randint(150, 200),
        random.randint(90, 120),
        random.randint(80, 89),
        random.randint(8, 10),
        random.choice(sintomas_alta),
        random.choice(condiciones),
        "ALTA"
    ])
    id_paciente += 1

columnas = [
    "id_paciente",
    "edad",
    "sexo",
    "temperatura_c",
    "frecuencia_cardiaca",
    "presion_sistolica",
    "presion_diastolica",
    "saturacion_oxigeno",
    "nivel_dolor",
    "sintoma",
    "condicion_cronica",
    "prioridad"
]

df = pd.DataFrame(datos, columns=columnas)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv(
    r"C:\xampp\htdocs\clasificacion_pacientes_ml\data\pacientes_balanceado.csv",
    index=False,
    encoding="utf-8"
)

print("Dataset generado correctamente")
print(df["prioridad"].value_counts())