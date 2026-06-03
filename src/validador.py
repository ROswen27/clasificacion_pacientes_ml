def validar_paciente(datos):
    errores = []
    advertencias = []

    # Edad
    if datos["edad"] < 0 or datos["edad"] > 120:
        errores.append("Edad fuera de rango clínico (0-120 años)")

    # Temperatura
    if datos["temperatura_c"] < 30 or datos["temperatura_c"] > 45:
        errores.append("Temperatura corporal no compatible con vida normal")

    elif datos["temperatura_c"] > 40:
        advertencias.append("Fiebre extremadamente alta")

    # Frecuencia cardíaca
    if datos["frecuencia_cardiaca"] < 30 or datos["frecuencia_cardiaca"] > 220:
        errores.append("Frecuencia cardíaca fuera de rango fisiológico")

    elif datos["frecuencia_cardiaca"] > 120:
        advertencias.append("Taquicardia detectada")

    # Presión arterial
    if datos["presion_sistolica"] < 70 or datos["presion_sistolica"] > 250:
        errores.append("Presión sistólica fuera de rango clínico")

    if datos["presion_diastolica"] < 40 or datos["presion_diastolica"] > 150:
        errores.append("Presión diastólica fuera de rango clínico")

    # Saturación de oxígeno
    if datos["saturacion_oxigeno"] < 50 or datos["saturacion_oxigeno"] > 100:
        errores.append("Saturación de oxígeno inválida")

    elif datos["saturacion_oxigeno"] < 90:
        advertencias.append("Hipoxemia (oxígeno bajo)")

    # Dolor
    if datos["nivel_dolor"] < 0 or datos["nivel_dolor"] > 10:
        errores.append("Nivel de dolor debe estar entre 0 y 10")

    elif datos["nivel_dolor"] >= 8:
        advertencias.append("Dolor severo")

    # Texto
    if not datos.get("sintoma"):
        advertencias.append("No se especificó síntoma")

    if not datos.get("condicion_cronica"):
        advertencias.append("No se especificó condición crónica")

    return {
        "errores": errores,
        "advertencias": advertencias,
        "valido": len(errores) == 0
    }