let pacienteEditando = null;

/* =========================
   CLASIFICAR / EDITAR
========================= */
async function clasificarPaciente() {

    const datos = {
        edad: parseInt(document.getElementById("edad").value),
        sexo: document.getElementById("sexo").value,
        temperatura_c: parseFloat(document.getElementById("temperatura").value),
        frecuencia_cardiaca: parseInt(document.getElementById("frecuencia").value),
        presion_sistolica: parseInt(document.getElementById("sistolica").value),
        presion_diastolica: parseInt(document.getElementById("diastolica").value),
        saturacion_oxigeno: parseInt(document.getElementById("oxigeno").value),
        nivel_dolor: parseInt(document.getElementById("dolor").value),
        sintoma: document.getElementById("sintoma").value,
        condicion_cronica: document.getElementById("cronica").value
    };

    let url = "/predecir";
    let method = "POST";

    if (pacienteEditando !== null) {
        url = `/paciente/${pacienteEditando}`;
        method = "PUT";
    }

    const respuesta = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(datos)
    });

    const resultado = await respuesta.json();

    let clase = "baja";

    if (resultado.prioridad === "ALTA") {
        clase = "alta";
    }

    if (resultado.prioridad === "MEDIA") {
        clase = "media";
    }

    document.getElementById("resultado").innerHTML = `
        <div id="reportePDF" style="padding:20px;border:1px solid #ccc;border-radius:10px;">

        <h3>ID Paciente: ${resultado.id || pacienteEditando}</h3>
            <h2 class="${clase}">
                Prioridad: ${resultado.prioridad}
            </h2>

            <p>
                ${resultado.descripcion}
            </p>

            <button onclick="exportarPDF()">
                Exportar PDF
            </button>

        </div>
    `;

    pacienteEditando = null;

    cargarPacientes();
}


/* =========================
   CARGAR HISTORIAL
========================= */
async function cargarPacientes() {

    const respuesta = await fetch(
        "/pacientes"
    );

    const pacientes = await respuesta.json();

    const filtro =
        document.getElementById("filtroPrioridad").value;

    let html = `
        <table border="1" width="100%" style="border-collapse:collapse;text-align:center;">
            <tr>
                <th>ID</th>
                <th>Edad</th>
                <th>Síntoma</th>
                <th>Prioridad</th>
                <th>Acciones</th>
            </tr>
    `;

    pacientes
        .filter(
            p => filtro === "TODOS" || p.prioridad === filtro
        )
        .forEach(paciente => {

            let color = "black";

            if (paciente.prioridad === "ALTA") {
                color = "red";
            }

            if (paciente.prioridad === "MEDIA") {
                color = "orange";
            }

            if (paciente.prioridad === "BAJA") {
                color = "green";
            }

            html += `
                <tr>
                    <td>${paciente.id}</td>

                    <td>${paciente.edad}</td>

                    <td>${paciente.sintoma}</td>

                    <td style="color:${color};font-weight:bold;">
                        ${paciente.prioridad}
                    </td>

                    <td style="white-space:nowrap;">
<button onclick="verReporte(${paciente.id})">
    Reporte
</button>

<button onclick="editarPaciente(${paciente.id})">
    Editar
</button>

<button onclick="eliminarPaciente(${paciente.id})">
    Eliminar
</button>

                    </td>
                </tr>
            `;
        });

    html += "</table>";

    document.getElementById("historial").innerHTML = html;
}


/* =========================
   EDITAR PACIENTE
========================= */
async function editarPaciente(id) {

    const respuesta = await fetch(
        `/paciente/${id}`
    );

    const paciente = await respuesta.json();

    document.getElementById("edad").value =
        paciente.edad;

    document.getElementById("sexo").value =
        paciente.sexo;

    document.getElementById("temperatura").value =
        paciente.temperatura_c;

    document.getElementById("frecuencia").value =
        paciente.frecuencia_cardiaca;

    document.getElementById("sistolica").value =
        paciente.presion_sistolica;

    document.getElementById("diastolica").value =
        paciente.presion_diastolica;

    document.getElementById("oxigeno").value =
        paciente.saturacion_oxigeno;

    document.getElementById("dolor").value =
        paciente.nivel_dolor;

    document.getElementById("sintoma").value =
        paciente.sintoma;

    document.getElementById("cronica").value =
        paciente.condicion_cronica;

    pacienteEditando = id;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

/* =========================
   VER REPORTE
========================= */
async function verReporte(id) {

    const respuesta = await fetch(
        `/paciente/${id}`
    );

    const paciente = await respuesta.json();

    document.getElementById("resultado").innerHTML = `
        <div id="reportePDF"
style="
background:#111827;
color:white;
padding:25px;
border-radius:15px;
box-shadow:0 8px 20px rgba(0,0,0,.4);
border-left:8px solid ${
    paciente.prioridad === 'ALTA'
        ? '#ef4444'
        : paciente.prioridad === 'MEDIA'
        ? '#f59e0b'
        : '#22c55e'
};
margin-top:20px;
">

            <h2>REPORTE MÉDICO</h2>
        <p>
            <strong>Fecha y Hora:</strong>
            ${new Date().toLocaleString("es-PE", {
                dateStyle: "full",
                timeStyle: "medium"
         })}
        </p>

<hr>
            <p><strong>ID Paciente:</strong> ${paciente.id}</p>

            <p><strong>Edad:</strong> ${paciente.edad}</p>

            <p><strong>Sexo:</strong> ${paciente.sexo}</p>

            <p><strong>Temperatura:</strong> ${paciente.temperatura_c} °C</p>

            <p><strong>Frecuencia Cardíaca:</strong> ${paciente.frecuencia_cardiaca} lpm</p>

            <p><strong>Presión Sistólica:</strong> ${paciente.presion_sistolica} mmHg</p>

            <p><strong>Presión Diastólica:</strong> ${paciente.presion_diastolica} mmHg</p>

            <p><strong>Saturación O₂:</strong> ${paciente.saturacion_oxigeno}%</p>

            <p><strong>Nivel Dolor:</strong> ${paciente.nivel_dolor}/10</p>

            <p><strong>Síntoma:</strong> ${paciente.sintoma}</p>

           <p><strong>Condición Crónica:</strong> ${paciente.condicion_cronica}</p>

<hr>

<h3>Evaluación Clínica</h3>

<p>
    ${paciente.descripcion}
</p>

<h3 style="
    color:
    ${paciente.prioridad === 'ALTA'
        ? 'red'
        : paciente.prioridad === 'MEDIA'
        ? 'orange'
        : 'green'};
">
    Prioridad: ${paciente.prioridad}
</h3>

            <button onclick="exportarPDF()">
                Exportar PDF
            </button>

        </div>
    `;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

/* =========================
   ELIMINAR PACIENTE
========================= */
async function eliminarPaciente(id) {

    const confirmar = confirm(
        "¿Desea eliminar este paciente?"
    );

    if (!confirmar) {
        return;
    }

    await fetch(
        `/paciente/${id}`,
        {
            method: "DELETE"
        }
    );

    cargarPacientes();
}


/* =========================
   EXPORTAR PDF
========================= */
async function exportarPDF() {

    const elemento =
        document.getElementById("reportePDF");

    const canvas = await html2canvas(
        elemento,
        {
            scale: 2
        }
    );

    const imgData =
        canvas.toDataURL("image/png");

    const { jsPDF } = window.jspdf;

    const pdf = new jsPDF(
        "p",
        "mm",
        "a4"
    );

    const imgWidth = 210;
    const imgHeight =
        (canvas.height * imgWidth) /
        canvas.width;

    pdf.addImage(
        imgData,
        "PNG",
        0,
        0,
        imgWidth,
        imgHeight
    );

    pdf.save(
        "reporte-paciente.pdf"
    );
}

/* =========================
   BUSCAR PACIENTE POR ID
========================= */
async function buscarPaciente() {

    const id = document.getElementById("buscarId").value;

    if (!id) {
        alert("Ingrese un ID");
        return;
    }

    const respuesta = await fetch(
        `/paciente/${id}`
    );

    const paciente = await respuesta.json();

    if (paciente.mensaje) {
        alert("Paciente no encontrado");
        return;
    }

    verReporte(id);
}

/* =========================
   INICIO
========================= */
cargarPacientes();