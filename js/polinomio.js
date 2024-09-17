// Función para generar un ejercicio de polinomios
function generarEjercicio() {
    const min = 1;
    const max = 10;
    const tiposEjercicios = ['suma', 'resta'];
    const tipo = tiposEjercicios[Math.floor(Math.random() * tiposEjercicios.length)];

    // Generar coeficientes aleatorios para los polinomios
    function generarCoeficientes() {
        return [
            Math.floor(Math.random() * (max - min + 1)) + min,
            Math.floor(Math.random() * (max - min + 1)) + min,
            Math.floor(Math.random() * (max - min + 1)) + min
        ];
    }

    let coeficientes1 = generarCoeficientes();
    let coeficientes2 = generarCoeficientes();
    let polinomio1 = `${coeficientes1[0]}x² + ${coeficientes1[1]}x + ${coeficientes1[2]}`;
    let polinomio2 = `${coeficientes2[0]}x² + ${coeficientes2[1]}x + ${coeficientes2[2]}`;

    let resultadoPolinomio;
    let resultado;

    if (tipo === 'suma') {
        resultadoPolinomio = `${coeficientes1[0] + coeficientes2[0]}x² + ${coeficientes1[1] + coeficientes2[1]}x + ${coeficientes1[2] + coeficientes2[2]}`;
        resultado = [coeficientes1[0] + coeficientes2[0], coeficientes1[1] + coeficientes2[1], coeficientes1[2] + coeficientes2[2]];
        document.getElementById('ejercicio').innerHTML = `Suma los polinomios: ${polinomio1} y ${polinomio2}.`;
    } else if (tipo === 'resta') {
        resultadoPolinomio = `${coeficientes1[0] - coeficientes2[0]}x² + ${coeficientes1[1] - coeficientes2[1]}x + ${coeficientes1[2] - coeficientes2[2]}`;
        resultado = [coeficientes1[0] - coeficientes2[0], coeficientes1[1] - coeficientes2[1], coeficientes1[2] - coeficientes2[2]];
        document.getElementById('ejercicio').innerHTML = `Resta los polinomios: ${polinomio1} y ${polinomio2}.`;
    }

    // Guardar el resultado en formato de array para la verificación
    window.resultado = resultado;
}

// Función para comprobar la respuesta del usuario
function comprobarRespuesta() {
    let respuestaUsuario = document.getElementById('respuestaConstruida').innerText.trim();

    // Construir la respuesta correcta en formato de texto
    let resultadoTexto = `${window.resultado[0]}x² + ${window.resultado[1]}x + ${window.resultado[2]}`;

    // Normalizar ambas respuestas para comparación
    respuestaUsuario = respuestaUsuario.replace(/\s+/g, '').toLowerCase();
    resultadoTexto = resultadoTexto.replace(/\s+/g, '').toLowerCase();

    if (respuestaUsuario === resultadoTexto) {
        document.getElementById('resultado').innerHTML = "¡Correcto!";
        document.getElementById('resultado').style.color = "green";
    } else {
        document.getElementById('resultado').innerHTML = `Incorrecto, la solución es ${resultadoTexto}.`;
        document.getElementById('resultado').style.color = "red";
    }

    generarEjercicio();  // Generar un nuevo ejercicio
    document.getElementById('respuestaConstruida').innerText = "";  // Limpiar la respuesta construida
}

// Función para agregar un carácter a la respuesta construida
function agregarCaracter(caracter) {
    let respuesta = document.getElementById('respuestaConstruida');
    respuesta.innerText += caracter;
}

// Función para borrar el último carácter de la respuesta construida
function borrarCaracter() {
    let respuesta = document.getElementById('respuestaConstruida');
    respuesta.innerText = respuesta.innerText.slice(0, -1);
}

// Función para cerrar la página
function cerrarPagina() {
    window.close();
}

// Generar un ejercicio al cargar la página
window.onload = generarEjercicio;
