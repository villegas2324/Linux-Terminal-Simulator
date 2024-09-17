const librosPorGrado = {
    1: [
        { title: "Ecuaciones de Primer Grado", cover: "img/icono1.png", pdf: "libros/algebra1.pdf", ejercicios: "ecuaciones.html"  },
        { title: "Operaciones Combinadas", cover: "img/icono1.png", pdf: "libros/algebra11.pdf", ejercicios: "combinadas.html" },
        { title: "Propiedades de los Triángulos", cover: "img/icono1.png", pdf: "libros/geometria1.pdf", ejercicios: "triangulos.html" }
    ],
    2: [
        { title: "Polinomios", cover: "img/icono2.png", pdf: "libros/algebra2.pdf", ejercicios: "polinomios.html"  },
        { title: "Congruencia de Triángulos", cover: "img/icono2.png", pdf: "libros/geometria2.pdf", ejercicios: "triangulos.html"  },
        { title: "Edades", cover: "img/icono2.png", pdf: "libros/rm2.pdf", ejercicios: "edades.html"  }
    ],
    3: [
        { title: "Cuadriláteros", cover: "img/icono3.png", pdf: "libros/geometria3.pdf", ejercicios: "https://www.matesfacil.com/interactivos/primaria/geometria/2D/identificar/paralelogramos/php1.php"  },
        { title: "Móviles", cover: "img/icono3.png", pdf: "libros/rm3.pdf", ejercicios: "https://www.cokitos.com/problema-de-ecuaciones-de-primer-grado/play/"  },
        { title: "Promedios", cover: "img/icono3.png", pdf: "libros/aritmetica3.pdf", ejercicios: "https://www.matesfacil.com/interactivos/primaria/fracciones/sumas/diferente/php1.php"  }
    ],
    4: [
        { title: "Factorización", cover: "img/icono4.png", pdf: "libros/algebra4.pdf", ejercicios: "https://www.matesfacil.com/interactivos/algebra-basica/nivel-7/php1.php"  },
        { title: "Porcentajes", cover: "img/icono4.png", pdf: "libros/rm4.pdf", ejercicios: "https://www.cokitos.com/operaciones-con-decimales/play/"  },
        { title: "Razones Trigonométricas de Ángulos Agudos", cover: "img/icono4.png", pdf: "libros/trigonometria4.pdf", ejercicios: "https://www.cokitos.com/partes-del-circulo-y-de-la-circunferencia/play/"  }
    ],
    5: [
        { title: "Divisibilidad", cover: "img/icono5.png", pdf: "libros/aritmetica5.pdf", ejercicios: "https://www.cokitos.com/operaciones-con-decimales/play/"  },
        { title: "Ángulos Verticales", cover: "img/icono5.png", pdf: "libros/trigonometria5.pdf", ejercicios: "https://www.cokitos.com/problema-de-ecuaciones-de-primer-grado/play/"  },
        { title: "Circunferencia", cover: "img/icono5.png", pdf: "libros/geometria5.pdf", ejercicios: "https://www.cokitos.com/partes-del-circulo-y-de-la-circunferencia/play/"  }
    ]
    // Puedes añadir más grados y libros aquí
};


function cargarLibros(grado) {
    const listaLibros = document.getElementById('lista-libros');
    listaLibros.innerHTML = ''; // Limpiar los libros actuales

    const libros = librosPorGrado[grado] || [];
    libros.forEach(libro => {
        const libroElemento = document.createElement('div');
        libroElemento.classList.add('libro');

        libroElemento.innerHTML = `
            <img src="${libro.cover}" alt="${libro.title}">
            <h2>${libro.title}</h2>
            <a href="${libro.pdf}" target="_blank" class="btn-ejercicios">Ver Ficha</a>
            <br>
            <a href="${libro.ejercicios}" target="_blank" class="btn-ejercicios">Resolver Ejercicios</a>
        `;

        listaLibros.appendChild(libroElemento);
    });

    // Modificar el tamaño de los iconos (ejemplo)
    modificarTamanoIconos('150px', '150px');
    
}

document.getElementById('grado').addEventListener('change', function() {
    const gradoSeleccionado = this.value;
    cargarLibros(gradoSeleccionado);
});

// Cargar libros del primer grado por defecto al inicio
document.addEventListener('DOMContentLoaded', () => {
    cargarLibros(1);
});

