from sqlalchemy import Column, Integer, String, Float

from database.db import Base


class Paciente(Base):

    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)

    edad = Column(Integer)
    sexo = Column(String)

    temperatura_c = Column(Float)

    frecuencia_cardiaca = Column(Integer)

    presion_sistolica = Column(Integer)

    presion_diastolica = Column(Integer)

    saturacion_oxigeno = Column(Integer)

    nivel_dolor = Column(Integer)

    sintoma = Column(String)

    condicion_cronica = Column(String)

    prioridad = Column(String)