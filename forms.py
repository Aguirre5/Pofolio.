# ==========================================
# IMPORTACIONES
# ==========================================

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    IntegerField,
    SelectField
)

from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
    URL,
    Email,
    ValidationError
)


# ==========================================
# VALIDACIONES PERSONALIZADAS
# ==========================================

# Solamente permitimos enlaces HTTP y HTTPS.
def validar_http(form, field):

    if not field.data.lower().startswith(
        ("http://", "https://")
    ):

        raise ValidationError(
            "El enlace debe comenzar con http:// o https://"
        )


# Eliminamos espacios innecesarios.
def limpiar_texto(valor):

    if isinstance(valor, str):
        return valor.strip()

    return valor


# ==========================================
# FORMULARIO DE INICIO DE SESIÓN
# ==========================================

class LoginForm(FlaskForm):

    username = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(max=80)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[DataRequired()]
    )

    submit = SubmitField("Iniciar sesión")


# ==========================================
# FORMULARIO DE ACCIONES PROTEGIDAS
# ==========================================

# Utilizado para cerrar sesión y eliminar registros.
class AccionForm(FlaskForm):

    submit = SubmitField("Confirmar")


# ==========================================
# FORMULARIO DEL PERFIL PERSONAL
# ==========================================

class PerfilForm(FlaskForm):

    nombre = StringField(
        "Nombre completo",
        filters=[limpiar_texto],
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    titulo = StringField(
        "Título profesional",
        validators=[Length(max=150)]
    )

    descripcion = TextAreaField(
        "Acerca de mí",
        validators=[Length(max=4000)]
    )

    ubicacion = StringField(
        "Ubicación",
        validators=[Length(max=150)]
    )

    email = StringField(
        "Correo electrónico",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            Email(),
            Length(max=150)
        ]
    )

    github = StringField(
        "Enlace a GitHub",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    linkedin = StringField(
        "Enlace a LinkedIn",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    foto = StringField(
        "URL de fotografía de perfil",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    banner = StringField(
        "URL del banner",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    submit = SubmitField("Guardar cambios")


# ==========================================
# FORMULARIO DE EXPERIENCIA LABORAL
# ==========================================

class ExperienciaForm(FlaskForm):

    puesto = StringField(
        "Puesto laboral",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    empresa = StringField(
        "Empresa",
        validators=[Length(max=150)]
    )

    periodo = StringField(
        "Período",
        validators=[Length(max=100)]
    )

    descripcion = TextAreaField(
        "Descripción de la experiencia",
        validators=[Length(max=4000)]
    )

    imagen = StringField(
        "URL de imagen o logo",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    submit = SubmitField("Guardar experiencia")


# ==========================================
# FORMULARIO DE EDUCACIÓN
# ==========================================

class EducacionForm(FlaskForm):

    titulo = StringField(
        "Título, carrera o curso",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    institucion = StringField(
        "Institución educativa",
        validators=[Length(max=150)]
    )

    periodo = StringField(
        "Período de formación",
        validators=[Length(max=100)]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[Length(max=4000)]
    )

    imagen = StringField(
        "URL del logo de la institución",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    submit = SubmitField("Guardar educación")


# ==========================================
# FORMULARIO DE HABILIDADES
# ==========================================

class HabilidadForm(FlaskForm):

    nombre = StringField(
        "Nombre de la habilidad",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    # El administrador seleccionará el tipo.
    tipo = SelectField(
        "Tipo de habilidad",
        choices=[
            ("hard", "Hard Skill"),
            ("soft", "Soft Skill"),
            ("idioma", "Idioma")
        ],
        validators=[DataRequired()]
    )

    # InputRequired permite ingresar el número cero.
    porcentaje = IntegerField(
        "Nivel de dominio (%)",
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=100,
                message="El porcentaje debe estar entre 0 y 100."
            )
        ]
    )

    submit = SubmitField("Guardar habilidad")


# ==========================================
# FORMULARIO DE PROYECTOS
# ==========================================

class ProyectoForm(FlaskForm):

    nombre = StringField(
        "Nombre del proyecto",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    fecha = StringField(
        "Fecha de realización",
        validators=[Length(max=100)]
    )

    descripcion = TextAreaField(
        "Descripción del proyecto",
        validators=[Length(max=4000)]
    )

    enlace = StringField(
        "Enlace al proyecto",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    imagen = StringField(
        "URL de imagen del proyecto",
        filters=[limpiar_texto],
        validators=[
            Optional(),
            URL(),
            validar_http,
            Length(max=500)
        ]
    )

    submit = SubmitField("Guardar proyecto")