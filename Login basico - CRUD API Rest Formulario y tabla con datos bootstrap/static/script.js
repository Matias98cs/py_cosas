document.addEventListener('DOMContentLoaded', function () {
    // Obtener la lista de calificaciones
    fetch('/api/calificaciones')
        .then(response => response.json())
        .then(data => mostrarcalificaciones(data));

    // Escuchar el evento de envío del formulario para agregar una nueva calificacion
    document.getElementById('nueva-calificacion-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const Nombre = document.getElementById('Nombre').value;
		const Clase = document.getElementById('Clase').value;
		const Materia = document.getElementById('Materia').value;
		const Calificacion = document.getElementById('Calificacion').value;
        agregarcalificacion(Nombre, Clase, Materia, Calificacion);
    });
});

function mostrarcalificaciones(calificaciones) {
    const calificacionesList = document.getElementById('calificaciones-list');
    calificacionesList.innerHTML = '';

    for (const calificacion of calificaciones) {
        const calificacionItem = document.createElement('div');
        calificacionItem.innerHTML = `
			<div class="row mt-2">
				<div class="col">${calificacion.Nombre}</div>
				<div class="col">${calificacion.Clase}</div>
				<div class="col">${calificacion.Materia}</div>
				<div class="col">${calificacion.Calificacion}</div>
				<div class="col"><button class="btn btn-danger btn-sm" onclick="eliminarcalificacion(${calificacion.id})">Eliminar</button></div>
			</div>
        `;
        calificacionesList.appendChild(calificacionItem);
    }
}

function agregarcalificacion(Nombre, Clase, Materia, Calificacion) {
    fetch('/api/calificaciones', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "Nombre": Nombre, "Clase": Clase, "Materia": Materia, "Calificacion": Calificacion})
    })
        .then(response => {
            if (response.ok) {
                // Si se obtiene un código 201 (creado satisfactoriamente)
                alert("Calificación agregada con éxito.");
                return response.json();
            } else {
                // Si la respuesta es un error
                throw new Error('Error al agregar calificación.');
            }
        })
        .then(data => {
            mostrarcalificaciones(data);
        }).catch(error => {
            alert("Error al agregar calificación.")
        });
}

function eliminarcalificacion(calificacionId) {
    var respuesta = confirm("¿Eliminar la calificación seleccionada?");
    if (respuesta) {
        fetch(`/api/calificaciones/${calificacionId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Si se obtiene un código 200 (éxito)
                alert("Calificación eliminada con éxito.");
                return response.json();
            } else {
                // Si la respuesta es un error
                throw new Error('Error al eliminar calificación.');
            }
        })
        .then(data => {
            mostrarcalificaciones(data);
        })
        .catch(error => {
            // Mostrar mensaje de error en caso de error en la solicitud
            alert(error.message);
        });
    }
}

