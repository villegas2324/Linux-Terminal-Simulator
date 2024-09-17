// Generar coeficientes enteros para la ecuación ax + b = c
function generarEcuacion() {
    // Generar coeficientes y términos enteros dentro de un rango
    let min = 1;
    let max = 10;

    a = Math.floor(Math.random() * (max - min + 1)) + min;  // Coeficiente de x (a) entre 1 y 10
    b = Math.floor(Math.random() * (max * 2 + 1)) - max;    // Término independiente (b) entre -10 y 10
    c = Math.floor(Math.random() * (max * 2 + 1)) - max;    // Resultado (c) entre -10 y 10

    // Asegurarse de que la ecuación sea válida (a != 0 y c - b sea divisible por a)
    while (a === 0 || (c - b) % a !== 0) {
        a = Math.floor(Math.random() * (max - min + 1)) + min;
        b = Math.floor(Math.random() * (max * 2 + 1)) - max;
        c = Math.floor(Math.random() * (max * 2 + 1)) - max;
    }

    // Mostrar la ecuación en el formato ax + b = c
    document.getElementById('ecuacion').innerHTML = `${a}x + (${b}) = ${c}`;
    solucion = (c - b) / a;  // Solución de la ecuación
}

// Función para comprobar la respuesta del usuario
function comprobarRespuesta() {
    let respuestaUsuario = parseFloat(document.getElementById('respuesta').value);

    if (respuestaUsuario === solucion) {
        document.getElementById('resultado').innerHTML = "¡Correcto!";
        document.getElementById('resultado').style.color = "green";
    } else {
        document.getElementById('resultado').innerHTML = `Incorrecto, la solución es x = ${solucion}.`;
        document.getElementById('resultado').style.color = "red";
    }

    generarEcuacion();  // Generar una nueva ecuación
    document.getElementById('respuesta').value = "";  // Limpiar la respuesta
}

// Función para cerrar la página
function cerrarPagina() {
    window.close();
}

// Generar una ecuación al cargar la página
window.onload = generarEcuacion;

