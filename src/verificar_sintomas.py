import pandas as pd

df = pd.read_csv(
    r"C:\xampp\htdocs\clasificacion_pacientes_ml\data\pacientes_balanceado.csv"
)

print(sorted(df["sintoma"].unique()))