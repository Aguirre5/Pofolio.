# Importamos clase principal de Flask-WTF.
# Crea forms, valida y protege contra CSRF.
# Clase base para crear formularios.
from flask_wtf import FlaskForm

# Texto, contraseña y botón.
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

# Importamos validadores ante vacío y longitud.
from wtforms.validators import (
    DataRequired,
    Length
)

#Formulario para iniciar sesión.
class LoginForm(FlaskForm):

    # Campo obligatorio: nombre.
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(
                message="Ingresá tu nombre de usuario."
            ),
            Length(
                max=80,
                message="Su nombre es demasiado largo."
            )
        ]
    )

    # Campo contraseña:
    # PasswordField oculta carácteres ingresados.
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(
                message="Ingresá tu contraseña."
            )
        ]
    )

    # Botón para enviar formulario.
    submit = SubmitField("Iniciar sesión")

#Formulario para acciones protegidas.
class AccionForm(FlaskForm):

    # Formulario para cerrar sesión
    submit = SubmitField("Confirmar")