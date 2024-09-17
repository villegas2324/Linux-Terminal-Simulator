// Función para generar un ejercicio de edades
function generarEjercicio() {
    const minEdad = 5;
    const maxEdad = 50;

    // Generar edades aleatorias para el ejercicio
    function generarEdad() {
        return Math.floor(Math.random() * (maxEdad - minEdad + 1)) + minEdad;
    }

    // Generar una edad inicial y calcular la edad final
    let edad1 = generarEdad();
    let edad2 = generarEdad();
    let edadFuturo = edad1 + edad2;

    // Crear la pregunta
    let pregunta = `Si la primera persona tiene ${edad1} años y la segunda persona tiene ${edad2} años, ¿cuántos años tendrán en total?`;
    document.getElementById('ejercicio').innerHTML = pregunta;

    // Guardar la respuesta correcta para comparación
    window.respuestaCorrecta = edadFuturo;
}

// Función para comprobar la respuesta del usuario
function comprobarRespuesta() {
    let respuestaUsuario = parseInt(document.getElementById('respuestaUsuario').value, 10);

    // Comparar la respuesta del usuario con la respuesta correcta
    if (respuestaUsuario === window.respuestaCorrecta) {
        document.getElementById('resultado').innerHTML = "¡Correcto!";
        document.getElementById('resultado').style.color = "green";
    } else {
        document.getElementById('resultado').innerHTML = `Incorrecto, la respuesta correcta es ${window.respuestaCorrecta}.`;
        document.getElementById('resultado').style.color = "red";
    }

    generarEjercicio();  // Generar un nuevo ejercicio
    document.getElementById('respuestaUsuario').value = "";  // Limpiar el campo de respuesta
}

// Función para cerrar la página
function cerrarPagina() {
    window.close();
}

// Generar un ejercicio al cargar la página
window.onload = generarEjercicio;
