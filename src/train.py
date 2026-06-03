import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Leer dataset
df = pd.read_csv(
    r"C:\xampp\htdocs\clasificacion_pacientes_ml\data\pacientes_balanceado.csv"
)
# Eliminar ID
df = df.drop("id_paciente", axis=1)

# Columnas categóricas
columnas_categoricas = [
    "sexo",
    "sintoma",
    "condicion_cronica",
    "prioridad"
]

encoders = {}

for columna in columnas_categoricas:
    encoder = LabelEncoder()

    df[columna] = encoder.fit_transform(df[columna])

    encoders[columna] = encoder

# Variables predictoras
X = df.drop("prioridad", axis=1)

# Variable objetivo
y = df["prioridad"]

# División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Modelo
modelo = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

modelo.fit(X_train, y_train)

# Predicción
y_pred = modelo.predict(X_test)

print("\nPRECISION:")
print(accuracy_score(y_test, y_pred))

print("\nREPORTE:")
print(classification_report(y_test, y_pred))

# Guardar modelo
joblib.dump(modelo, "models/modelo.pkl")

# Guardar encoders
joblib.dump(encoders, "models/encoders.pkl")

print("\nModelo guardado correctamente")