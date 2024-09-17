// Generar una operación combinada con operaciones aleatorias y resultados enteros
function generarOperacion() {
    const operaciones = ['+', '-', '*', '/'];
    const min = 1;
    const max = 10;

    // Generar números enteros aleatorios
    let num1 = Math.floor(Math.random() * (max - min + 1)) + min;
    let num2 = Math.floor(Math.random() * (max - min + 1)) + min;
    let num3 = Math.floor(Math.random() * (max - min + 1)) + min;

    // Seleccionar dos operaciones aleatorias
    let op1 = operaciones[Math.floor(Math.random() * operaciones.length)];
    let op2 = operaciones[Math.floor(Math.random() * operaciones.length)];

    // Asegurarse de que el resultado sea un entero
    let expresion;
    let resultado;

    do {
        // Generar números y operaciones
        num1 = Math.floor(Math.random() * (max - min + 1)) + min;
        num2 = Math.floor(Math.random() * (max - min + 1)) + min;
        num3 = Math.floor(Math.random() * (max - min + 1)) + min;

        op1 = operaciones[Math.floor(Math.random() * operaciones.length)];
        op2 = operaciones[Math.floor(Math.random() * operaciones.length)];

        expresion = `(${num1} ${op1} ${num2}) ${op2} ${num3}`;

        // Evaluar la expresión
        try {
            resultado = eval(expresion);

            // Verificar si el resultado es un entero
            if (Number.isInteger(resultado)) {
                break;
            }
        } catch (e) {
            console.error('Error al evaluar la expresión:', e);
            resultado = NaN;
        }
    } while (!Number.isInteger(resultado));

    // Mostrar la operación
    document.getElementById('operacion').innerHTML = expresion;

    // Guardar el resultado
    window.resultado = resultado;  // Guardar en variable global
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

    generarOperacion();  // Generar una nueva operación
    document.getElementById('respuesta').value = "";  // Limpiar la respuesta
}


// Función para cerrar la página
function cerrarPagina() {
    window.close();
}

// Generar una operación al cargar la página
window.onload = generarOperacion;
