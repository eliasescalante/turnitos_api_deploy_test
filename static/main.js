const resultado = document.getElementById("resultado");

function mostrar(data) {
    resultado.textContent = JSON.stringify(data, null, 2);
}

// GET /medicos
function getMedicos() {
    fetch("/medicos")
        .then(res => res.json())
        .then(data => mostrar(data))
        .catch(err => mostrar(err));
}

// GET /turnos/<medico_id>
function getTurnos() {
    const medicoId = prompt("Ingrese ID del médico:");
    if (!medicoId) return;

    fetch(`/turnos/${medicoId}`)
        .then(res => res.json())
        .then(data => mostrar(data))
        .catch(err => mostrar(err));
}

// POST /turnos
function reservarTurno() {
    const medico_id = document.getElementById("medico_id").value;
    const fechaInput = document.getElementById("fecha_hora").value;
    const paciente = document.getElementById("paciente").value;

    if (!medico_id || !fechaInput || !paciente) {
        alert("Complete todos los campos");
        return;
    }

    const fecha_hora = fechaInput.replace("T", " ") + ":00";

    fetch("/turnos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            medico_id,
            fecha_hora,
            paciente
        })
    })
    .then(async res => {
        const data = await res.json();
        mostrar(data);
    })
    .catch(err => mostrar(err));
}
