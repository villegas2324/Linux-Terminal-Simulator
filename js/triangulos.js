// Función para generar un ejercicio de triángulo
function generarEjercicio() {
    const min = 1;
    const max = 10;
    const tiposEjercicios = ['area', 'angulo'];
    const tipo = tiposEjercicios[Math.floor(Math.random() * tiposEjercicios.length)];

    if (tipo === 'area') {
        // Generar base y altura enteros aleatorios
        let base = Math.floor(Math.random() * (max - min + 1)) + min;
        let altura = Math.floor(Math.random() * (max - min + 1)) + min;

        // Calcular el área
        let area = (base * altura) / 2;
        while (!Number.isInteger(area)) {
            base = Math.floor(Math.random() * (max - min + 1)) + min;
            altura = Math.floor(Math.random() * (max - min + 1)) + min;
            area = (base * altura) / 2;
        }

        // Mostrar el ejercicio
        document.getElementById('ejercicio').innerHTML = `Calcula el área de un triángulo con base = ${base} y altura = ${altura}.`;

        // Guardar el resultado
        window.resultado = area;

    } else if (tipo === 'angulo') {
        // Generar dos ángulos enteros aleatorios (entre 1 y 89 grados)
        let angulo1 = Math.floor(Math.random() * 89) + 1;
        let angulo2 = Math.floor(Math.random() * (90 - angulo1)) + 1;

        // Calcular el ángulo desconocido
        let anguloDesconocido = 180 - (angulo1 + angulo2);

        // Mostrar el ejercicio
        document.getElementById('ejercicio').innerHTML = `Calcula el ángulo desconocido en un triángulo donde los otros dos ángulos son ${angulo1}° y ${angulo2}°.`;

        // Guardar el resultado
        window.resultado = anguloDesconocido;
    }
}

// Función para comprobar la respuesta del usuario
function comprobarRespuesta() {
    let respuestaUsuario = parseInt(document.getElementById('respuesta').value);

    if (respuestaUsuario === window.resultado) {
        document.getElementById('resultado').innerHTML = "¡Correcto!";
        document.getElementById('resultado').style.color = "green";
    } else {
        document.getElementById('resultado').innerHTML = `Incorrecto, la solución es ${window.resultado}.`;
        document.getElementById('resultado').style.color = "red";
    }

    generarEjercicio();  // Generar un nuevo ejercicio
    document.getElementById('respuesta').value = "";  // Limpiar la respuesta
}

// Función para cerrar la página
function cerrarPagina() {
    window.close();
}

// Generar un ejercicio al cargar la página
window.onload = generarEjercicio;
