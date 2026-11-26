// Esperamos a que el documento HTML esté cargado.
document.addEventListener("DOMContentLoaded", () => {

    // Obtenemos el botón y el campo de contraseña.
    const boton = document.getElementById("togglePassword");

    const password = document.getElementById("password");

    // Comprobamos que ambos elementos existan.
    if (!boton || !password) {

        return;

    }

    // Detectamos cuando se presiona el botón.
    boton.addEventListener("click", () => {

        // Comprobamos si la contraseña está oculta.
        const oculta = password.type === "password";

        // Alternamos entre texto visible y contraseña.
        password.type = oculta ? "text" : "password";

        // Obtenemos el icono del botón.
        const icono = boton.querySelector("i");

        // Actualizamos los atributos de accesibilidad.
        boton.setAttribute(
            "aria-pressed",
            String(oculta)
        );

        boton.setAttribute(
            "aria-label",
            oculta
                ? "Ocultar contraseña"
                : "Mostrar contraseña"
        );

    });

});