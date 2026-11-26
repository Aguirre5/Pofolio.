// CRUD.

document.addEventListener("DOMContentLoaded", () => {


    // Eliminacionón form.

    const formulariosEliminar = document.querySelectorAll(
        ".form-eliminar"
    );

    formulariosEliminar.forEach(formulario => {

        formulario.addEventListener("submit", evento => {

            // Solicitamos confirmación al administrador.
            const confirmar = window.confirm(
                "¿Estás seguro de que deseás eliminar este elemento? Esta acción no se puede deshacer."
            );

            // Si cancela, impedimos el envío.
            if (!confirmar) {

                evento.preventDefault();

            }

        });

    });


    // Config. ventanas.

    const modalElemento = document.getElementById(
        "modalEdicion"
    );

    const frame = document.getElementById(
        "frameEdicion"
    );

    // Si estamos navegando como visitantes,
    // no existirán estos elementos.
    if (!modalElemento || !frame || !window.bootstrap) {

        return;

    }

    // Creamos una instancia del modal de Bootstrap.
    const modal = new bootstrap.Modal(
        modalElemento
    );

    let editando = false;


    // Abrir forms.

    const botonesEdicion = document.querySelectorAll(
        "[data-editar]"
    );

    botonesEdicion.forEach(boton => {

        boton.addEventListener("click", evento => {

            // Evitamos abandonar la página principal.
            evento.preventDefault();

            editando = true;

            // Recuperamos la URL del formulario.
            const url = new URL(boton.href);

            // Indicamos al backend que se está
            // utilizando una ventana modal.
            url.searchParams.set("modal", "1");

            // Cargamos el formulario dentro del iframe.
            frame.src = url.href;

            // Mostramos la ventana.
            modal.show();

        });

    });


    // ¿Se guardó?

    frame.addEventListener("load", () => {

        if (!editando) {

            return;

        }

        try {

            // Recuperamos la URL actual del iframe.
            const url = new URL(
                frame.contentWindow.location.href
            );

            // Si la sesión expiró, volvemos al login.
            if (url.pathname === frame.dataset.login) {

                window.location.assign(
                    frame.dataset.login
                );

                return;

            }

            // Comprobamos si la edición finalizó.
            if (url.pathname === frame.dataset.completa) {

                editando = false;

                // Recuperamos la sección modificada.
                const seccion = url.searchParams.get(
                    "seccion"
                );

                const permitidas = [

                    "acerca",

                    "experiencia",

                    "educacion",

                    "habilidades",

                    "proyectos"

                ];

                // Regresamos a la sección modificada.
                if (permitidas.includes(seccion)) {

                    window.location.hash = seccion;

                }

                // Actualizamos el portfolio para
                // recuperar los nuevos datos de MySQL.
                window.location.reload();

            }

        } catch (error) {

            console.error(
                "Error al actualizar el portfolio:",
                error
            );

        }

    });


    // Limpia ventana.

    modalElemento.addEventListener(
        "hidden.bs.modal",
        () => {

            editando = false;

            // Eliminamos el formulario anterior.
            frame.src = "about:blank";

        }
    );

});