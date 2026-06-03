import pandas as pd

df = pd.read_csv(
    r"C:\xampp\htdocs\clasificacion_pacientes_ml\data\pacientes.csv"
)

print("=== PRIMERAS FILAS ===")
print(df.head())

print("\n=== INFORMACION ===")
print(df.info())

print("\n=== VALORES NULOS ===")
print(df.isnull().sum())

print("\n=== DISTRIBUCION DE PRIORIDAD ===")
print(df["prioridad"].value_counts())