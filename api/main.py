from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import PacienteSchema
from src.predict import predecir_paciente
from src.explicador import generar_explicacion
from src.validador import validar_paciente

from database.db import engine, SessionLocal
from database.models import Base, Paciente

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clasificación Automática de Pacientes",
    version="1.0"
)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return FileResponse("frontend/index.html")


# =========================
# PREDICCIÓN PRINCIPAL
# =========================
@app.post("/predecir")
def predecir(data: PacienteSchema):

    datos = data.dict()

    validacion = validar_paciente(datos)

    if not validacion["valido"]:
        return {
            "error": "Datos clínicamente inválidos",
            "detalles": validacion
        }

    prioridad = predecir_paciente(datos)

    descripcion = generar_explicacion(
        datos,
        prioridad
    )

    db = SessionLocal()

    nuevo_paciente = Paciente(
        edad=data.edad,
        sexo=data.sexo,
        temperatura_c=data.temperatura_c,
        frecuencia_cardiaca=data.frecuencia_cardiaca,
        presion_sistolica=data.presion_sistolica,
        presion_diastolica=data.presion_diastolica,
        saturacion_oxigeno=data.saturacion_oxigeno,
        nivel_dolor=data.nivel_dolor,
        sintoma=data.sintoma,
        condicion_cronica=data.condicion_cronica,
        prioridad=prioridad
    )

    db.add(nuevo_paciente)
    db.commit()

    # Obtener ID generado automáticamente
    db.refresh(nuevo_paciente)

    db.close()

    return {
        "id": nuevo_paciente.id,
        "prioridad": prioridad,
        "descripcion": descripcion,
        "validacion": validacion
    }


# =========================
# LISTAR PACIENTES
# =========================
@app.get("/pacientes")
def listar_pacientes():

    db = SessionLocal()
    pacientes = db.query(Paciente).all()
    db.close()

    return [
        {
            "id": p.id,
            "edad": p.edad,
            "sexo": p.sexo,
            "temperatura_c": p.temperatura_c,
            "frecuencia_cardiaca": p.frecuencia_cardiaca,
            "presion_sistolica": p.presion_sistolica,
            "presion_diastolica": p.presion_diastolica,
            "saturacion_oxigeno": p.saturacion_oxigeno,
            "nivel_dolor": p.nivel_dolor,
            "sintoma": p.sintoma,
            "condicion_cronica": p.condicion_cronica,
            "prioridad": p.prioridad
        }
        for p in pacientes
    ]


# =========================
# OBTENER PACIENTE
# =========================
@app.get("/paciente/{id_paciente}")
def obtener_paciente(id_paciente: int):

    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.id == id_paciente
    ).first()

    if paciente is None:
        db.close()

        return {
            "mensaje": "Paciente no encontrado"
        }

    datos = {
        "edad": paciente.edad,
        "sexo": paciente.sexo,
        "temperatura_c": paciente.temperatura_c,
        "frecuencia_cardiaca": paciente.frecuencia_cardiaca,
        "presion_sistolica": paciente.presion_sistolica,
        "presion_diastolica": paciente.presion_diastolica,
        "saturacion_oxigeno": paciente.saturacion_oxigeno,
        "nivel_dolor": paciente.nivel_dolor,
        "sintoma": paciente.sintoma,
        "condicion_cronica": paciente.condicion_cronica
    }

    descripcion = generar_explicacion(
        datos,
        paciente.prioridad
    )

    db.close()

    return {
        "id": paciente.id,
        "edad": paciente.edad,
        "sexo": paciente.sexo,
        "temperatura_c": paciente.temperatura_c,
        "frecuencia_cardiaca": paciente.frecuencia_cardiaca,
        "presion_sistolica": paciente.presion_sistolica,
        "presion_diastolica": paciente.presion_diastolica,
        "saturacion_oxigeno": paciente.saturacion_oxigeno,
        "nivel_dolor": paciente.nivel_dolor,
        "sintoma": paciente.sintoma,
        "condicion_cronica": paciente.condicion_cronica,
        "prioridad": paciente.prioridad,
        "descripcion": descripcion
    }


# =========================
# ACTUALIZAR PACIENTE
# =========================
@app.put("/paciente/{id_paciente}")
def actualizar_paciente(id_paciente: int, data: PacienteSchema):

    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.id == id_paciente
    ).first()

    if paciente is None:
        db.close()

        return {
            "mensaje": "Paciente no encontrado"
        }

    datos = data.dict()

    prioridad = predecir_paciente(datos)

    descripcion = generar_explicacion(
        datos,
        prioridad
    )

    paciente.edad = data.edad
    paciente.sexo = data.sexo
    paciente.temperatura_c = data.temperatura_c
    paciente.frecuencia_cardiaca = data.frecuencia_cardiaca
    paciente.presion_sistolica = data.presion_sistolica
    paciente.presion_diastolica = data.presion_diastolica
    paciente.saturacion_oxigeno = data.saturacion_oxigeno
    paciente.nivel_dolor = data.nivel_dolor
    paciente.sintoma = data.sintoma
    paciente.condicion_cronica = data.condicion_cronica
    paciente.prioridad = prioridad

    db.commit()
    db.close()

    return {
        "mensaje": "Paciente actualizado correctamente",
        "prioridad": prioridad,
        "descripcion": descripcion
    }


# =========================
# ELIMINAR PACIENTE
# =========================
@app.delete("/paciente/{id_paciente}")
def eliminar_paciente(id_paciente: int):

    db = SessionLocal()

    paciente = db.query(Paciente).filter(
        Paciente.id == id_paciente
    ).first()

    if paciente is None:
        db.close()

        return {
            "mensaje": "Paciente no encontrado"
        }

    db.delete(paciente)

    db.commit()
    db.close()

    return {
        "mensaje": "Paciente eliminado correctamente"
    }