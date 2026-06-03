def generar_explicacion(datos, prioridad):

    razonamientos = []

    # Evaluación clínica básica
    if datos["temperatura_c"] >= 39:
        razonamientos.append(
            f"presenta fiebre alta ({datos['temperatura_c']}°C)"
        )

    if datos["frecuencia_cardiaca"] >= 120:
        razonamientos.append(
            f"frecuencia cardíaca elevada ({datos['frecuencia_cardiaca']} lpm)"
        )

    if datos["presion_sistolica"] >= 160:
        razonamientos.append(
            f"presión sistólica alta ({datos['presion_sistolica']} mmHg)"
        )

    if datos["saturacion_oxigeno"] < 90:
        razonamientos.append(
            f"saturación de oxígeno baja ({datos['saturacion_oxigeno']}%)"
        )

    if datos["nivel_dolor"] >= 8:
        razonamientos.append(
            f"dolor intenso (nivel {datos['nivel_dolor']}/10)"
        )

    if datos["condicion_cronica"].lower() != "ninguna":
        razonamientos.append(
            f"condición crónica reportada: {datos['condicion_cronica']}"
        )

    sintoma = datos.get("sintoma", "no especificado")

    texto_base = (
        f"El paciente fue clasificado con prioridad {prioridad}. "
        f"El síntoma principal es '{sintoma}'. "
    )

    if razonamientos:
        texto_base += "Se observan los siguientes hallazgos: " + ", ".join(razonamientos) + ". "
    else:
        texto_base += "No se observan signos clínicos de alarma relevantes. "

    # 🔴 CONCLUSIÓN COHERENTE SEGÚN PRIORIDAD
    if prioridad == "ALTA":
        texto_base += (
            "El conjunto de hallazgos indica posible riesgo agudo, por lo que se recomienda atención médica inmediata."
        )

    elif prioridad == "MEDIA":
        texto_base += (
            "Los hallazgos sugieren condición moderada que requiere evaluación médica prioritaria."
        )

    else:  # BAJA
        texto_base += (
            "Los signos vitales se encuentran dentro de rangos estables, sin evidencia de urgencia inmediata."
        )

    return texto_base