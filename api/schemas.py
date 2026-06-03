from pydantic import BaseModel


class PacienteSchema(BaseModel):
    edad: int
    sexo: str
    temperatura_c: float
    frecuencia_cardiaca: int
    presion_sistolica: int
    presion_diastolica: int
    saturacion_oxigeno: int
    nivel_dolor: int
    sintoma: str
    condicion_cronica: str