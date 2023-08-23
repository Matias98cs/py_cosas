document.addEventListener('DOMContentLoaded', function () {
    obtener_personas();

    // Escuchar el evento de envío del formulario para agregar una nueva persona
    document.getElementById('nueva-persona-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const nombre = document.getElementById('nombre').value;
        const apellido = document.getElementById('apellido').value;
        const email = document.getElementById('email').value;
        //const birthdate = document.getElementById('birthdate').value;
        const personal_id = document.getElementById('personal_id').value;
        const genero_id = parseInt(document.getElementById('genero_id').value);
        //const lugar_id = parseInt(document.getElementById('lugar_id').value);
        agregarPersona(nombre, apellido, email, personal_id, genero_id);
    });
});

function obtener_personas(){
    // Obtener la lista de personas
    fetch('/api/personas')
        .then(response => response.json())
        .then(data => mostrarPersonas(data));
}

function mostrarPersonas(personas) {
    const personasList = document.getElementById('personas-list');
    personasList.innerHTML = '';

    for (const persona of personas) {
        const personaItem = document.createElement('div');
        personaItem.innerHTML = `
			<div class="row mt-2">
				<div class="col-2 text-wrap">${persona.nombre}</div>
				<div class="col-2 text-wrap">${persona.apellido}</div>
				<div class="col-2 text-wrap">${persona.email}</div>
				<div class="col-2 text-wrap text-right">${persona.personal_id}</div>
				<div class="col-2 text-wrap">${persona.genero}</div>
				<div class="col-2"><button class="btn btn-danger btn-sm" onclick="eliminarPersona(${persona.id})">Eliminar</button></div>
			</div>
        `;
        personasList.appendChild(personaItem);
    }
}

function agregarPersona(nombre, apellido, email, personal_id, genero_id) {
    fetch('/api/personas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"nombre": nombre,"apellido": apellido,"email": email,"personal_id": personal_id,"genero_id": genero_id})
    })
        .then(response => {
            if (response.ok) {
                // Si se obtiene un código 201 (creado satisfactoriamente)
                alert("Persona agregada con éxito.");
                obtener_personas();
            } else {
                // Si la respuesta es un error
                throw new Error('Error al agregar persona.');
            }
        })
        .catch(error => {
            alert("Error al agregar persona.")
        });
}

function eliminarPersona(personaId) {
    var respuesta = confirm("¿Eliminar la persona seleccionada?");
    if (respuesta) {
        fetch(`/api/personas/${personaId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Si se obtiene un código 200 (éxito)
                alert("Persona eliminada con éxito.");
                obtener_personas();
            } else {
                // Si la respuesta es un error
                throw new Error('Error al eliminar persona.\n');
            }
        })
        .catch(error => {
            // Mostrar mensaje de error en caso de error en la solicitud
            alert(error.message);
        });
    }
}
