import click

from flask import send_from_directory

# Flask.
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    request
)

# Herramientas para administrar sesiones de usuarios.
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

# Protección contra solicitudes fraudulentas.
from flask_wtf.csrf import CSRFProtect

# Importamos nuestros formularios.
from forms import (
    LoginForm,
    AccionForm,
    PerfilForm,
    ExperienciaForm,
    EducacionForm,
    HabilidadForm,
    ProyectoForm
)

# Permite controlar errores de la base de datos.
from sqlalchemy.exc import SQLAlchemyError

# Herram. SQLAlchemy.
from sqlalchemy import text, inspect

# Herram. diseño físico.
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql

# Permite trabajr on archivos y carpetas.
from pathlib import Path

# config.
from config import Config

# y todos nuestros modelos.
from tables import (
    db,
    Usuario,
    Perfil,
    Experiencia,
    Educacion,
    Habilidad,
    Proyecto,
    Contenido,
    TarjetaExperiencia,
    TarjetaEducacion,
    TarjetaProyecto,
    presentar_contenido
)
#-----------------------------------------
#Aplicación:

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

# -----------------------------------------
#Configuración de seguridad.

# Activamos CSRF para toda la aplicación.
csrf = CSRFProtect(app)

# Creamos el administrador de sesiones.
login_manager = LoginManager(app)

# Indicamos a qué ruta deberá dirigirse un usuario
# cuando intente acceder sin estar autenticado.
login_manager.login_view = "login"

# Mensaje que aparecerá al intentar ingresar
# a una sección protegida.
login_manager.login_message = (
    "Debés iniciar sesión para acceder a esta sección."
)

login_manager.login_message_category = "warning"

# Protección adicional de las sesiones.
login_manager.session_protection = "strong"


# -----------------------------------------
#Recuperación de usuario desde la sesión.

@login_manager.user_loader
def cargar_usuario(usuario_id):

    # Flask-Login utiliza el ID almacenado en la sesión
    # para recuperar el usuario desde MySQL.

    try:

        return db.session.get(
            Usuario,
            int(usuario_id)
        )

    except (ValueError, TypeError):

        return None

# Configuración CRUD-

# Cada sección tiene asociado:
# 1. Modelo de MySQL.
# 2. Formulario Flask-WTF.
# 3. Nombre descriptivo.
# 4. Identificador dentro del HTML.

SECCIONES = {

    "experiencias": (
        Experiencia,
        ExperienciaForm,
        "experiencia laboral",
        "experiencia"
    ),

    "educacion": (
        Educacion,
        EducacionForm,
        "formación académica",
        "educacion"
    ),

    "habilidades": (
        Habilidad,
        HabilidadForm,
        "habilidad",
        "habilidades"
    ),

    "proyectos": (
        Proyecto,
        ProyectoForm,
        "proyecto",
        "proyectos"
    )

}


#-----------------------------------------
#Ruta principal Portfolio.

@app.route("/")
def index():

    # Recuperamos el perfil personal.
    perfil = Perfil.query.order_by(
        Perfil.id
    ).first()

    # Comprobamos que el portfolio esté inicializado.
    if perfil is None:

        return "Portfolio sin inicializar.", 503

    # Identificador del propietario del portfolio.
    uid = perfil.usuario_id


    # ---------------------------------------
    # Consultas SQL.

    # Recuperamos todas las experiencias laborales.
    experiencias = Experiencia.query.filter_by(
        usuario_id=uid
    ).order_by(
        Experiencia.id.desc()
    ).all()

    # Recuperamos la formación académica.
    educacion = Educacion.query.filter_by(
        usuario_id=uid
    ).order_by(
        Educacion.id.desc()
    ).all()

    # Recuperamos las habilidades.
    habilidades = Habilidad.query.filter_by(
        usuario_id=uid
    ).order_by(
        Habilidad.id
    ).all()

    # Recuperamos los proyectos realizados.
    proyectos = Proyecto.query.filter_by(
        usuario_id=uid
    ).order_by(
        Proyecto.id.desc()
    ).all()


    # -------------------------------------------
    #Polimorfismo.
    # Utilizamos una misma función para presentar
    # diferentes tipos de contenido.

    tarjetas = {

        "experiencias": [

            (
                item,
                presentar_contenido(
                    TarjetaExperiencia(item)
                )
            )

            for item in experiencias

        ],

        "educacion": [

            (
                item,
                presentar_contenido(
                    TarjetaEducacion(item)
                )
            )

            for item in educacion

        ],

        "proyectos": [

            (
                item,
                presentar_contenido(
                    TarjetaProyecto(item)
                )
            )

            for item in proyectos

        ]

    }


    # ======================================
    # COMPROBAR IMÁGENES LOCALES
    # ======================================

    # Verificamos si existe una fotografía de perfil.
    foto_local = Path(
        app.static_folder,
        "img",
        "perfil.webp"
    ).is_file()

    # Verificamos si existe un banner personalizado.
    banner_local = Path(
        app.static_folder,
        "img",
        "banner.webp"
    ).is_file()

    # Jinja2 recibe.

    # Comprobamos si el CV se encuentra disponible.
    cv_disponible = Path(
        app.static_folder,
        "docs",
        "cv.pdf"
    ).is_file()


    return render_template(

        "index.html",

        perfil=perfil,

        tarjetas=tarjetas,

        habilidades=habilidades,

        accion=AccionForm(),

        foto_local=foto_local,

        banner_local=banner_local,

        cv_disponible=cv_disponible

    )


#Conexión MYSQL prueba.
@app.cli.command("test-db")
def probar_base_datos():
    try:
        # Consulta sencilla.
        resultado = db.session.execute(
            text("SELECT 1")
        ).scalar()

        # Comprobamos conexión.
        if resultado == 1:
            print("Conexion con MySQL exitosa.")

    except Exception as error:
        # Mostramos error local.
        print("Error de conexion:", error)
        raise SystemExit(1)

    finally:
        # Liberamos sesión de bd.
        db.session.remove()


#Tablas.

@app.cli.command("init-db")
def inicializar_db():
    db.create_all()
    print("Tablas creadas correctamente.")

#Tablas existentes.

@app.cli.command("list-db")
def listar_tablas():

    # Inspeccionamos db.
    inspector = inspect(db.engine)

    # Nombres de las tablas.
    tablas = inspector.get_table_names()

    print("\nTABLAS DE LA BASE DE DATOS")
    print("--------------------------")

    for tabla in tablas:

        print("-", tabla)

    print("\nCantidad de tablas:", len(tablas))

#Diseño físico:

@app.cli.command("export-sql")
def exportar_sql():

    # Creamos carpeta de documentación.
    # si todavía no existe:
    carpeta = Path(app.root_path) / "documentacion"
    carpeta.mkdir(exist_ok=True)

    # Dirección del archivo SQL.
    archivo = carpeta / "database.sql"

    # Encabezado del documento.
    instrucciones = [
        "-- Proyecto Integrador P. Portfolio",
        "-- Diseño físico db MySQL.",
        ""
    ]

    # Recorremos las tablas respetando el orden
    # de dependencias y claves foráneas.
    for tabla in db.metadata.sorted_tables:

        # Convertimos cada modelo a código SQL.
        sentencia = CreateTable(
            tabla,
            if_not_exists=True
        ).compile(
            dialect=mysql.dialect()
        )

        instrucciones.append(
            str(sentencia).strip() + ";"
        )

        instrucciones.append("")

    # Guardamos diseño físico.
    archivo.write_text(
        "\n".join(instrucciones),
        encoding="utf-8"
    )

    print("Diseño físico exportado.")
    print("Archivo:", archivo)

#Agregado de abstracto POO:

@app.cli.command("test-poo")
def probar_poo():

    # Creamos objetos de prueba.

    experiencia = Experiencia(
        puesto="Desarrollador",
        empresa="Empresa de prueba"
    )

    educacion = Educacion(
        titulo="Curso de Python",
        institucion="Institucion de prueba"
    )

    proyecto = Proyecto(
        nombre="Portfolio Full Stack",
        fecha="2026"
    )

    # Creamos objetos de clases derivadas.
    contenidos = [

        TarjetaExperiencia(experiencia),

        TarjetaEducacion(educacion),

        TarjetaProyecto(proyecto)

    ]

    print("\nPRUEBA")

    # Aplicamos la misma función a distintos objetos.
    for contenido in contenidos:

        datos = presentar_contenido(contenido)

        print("\nClase:", type(contenido).__name__)

        print("Titulo:", datos["titulo"])

        print("Detalle:", datos["detalle"])

    print("\nPrueba finalizada.")

# -----------------------------------------
#Admin creation.

@app.cli.command("crear-admin")

# Solicitamos datos desde la terminal.
@click.option("--username", prompt="Usuario")

@click.option(
    "--password",
    prompt="Contraseña",
    hide_input=True,
    confirmation_prompt=True
)

@click.option("--nombre", prompt="Nombre completo")

def crear_admin(username, password, nombre):

    # Eliminamos espacios innecesarios.
    username = username.strip()
    nombre = nombre.strip()

    # Validamos campos obligatorios.
    if not username or len(username) > 80:

        raise click.ClickException(
            "El nombre de usuario debe tener entre 1 y 80 caracteres."
        )

    if not nombre or len(nombre) > 100:

        raise click.ClickException(
            "El nombre completo debe tener entre 1 y 100 caracteres."
        )

    # Comprobamos administrador.
    if Usuario.query.first() is not None:

        raise click.ClickException(
            "El portfolio ya tiene un administrador."
        )

    # Validamos longitud de contraseña.
    if len(password) < 12:

        raise click.ClickException(
            "La contraseña debe tener al menos 12 caracteres."
        )

    # Creamos una instancia del modelo Usuario.
    usuario = Usuario(
        username=username
    )

    # Generamos hash:
    usuario.establecer_password(password)

    try:

        # Agregamos usuario a la sesión.
        db.session.add(usuario)

        # Obtenemos el ID generado por MySQL,
        # sin confirmar todavía la transacción.
        db.session.flush()

        # Creamos perfil personal asociado.
        perfil = Perfil(

            usuario_id=usuario.id,

            nombre=nombre,

            titulo="Portfolio profesional",

            descripcion="Completar presentación personal."

        )

        # Agregamos el perfil a la sesión.
        db.session.add(perfil)

        # Confirmamos ambos registros en MySQL.
        db.session.commit()

        click.echo("\nAdministrador creado correctamente.")
        click.echo("Perfil personal creado correctamente.")

    except Exception:

        # Si ocurre un error, deshacemos los cambios.
        db.session.rollback()
        raise click.ClickException(
            "No se pudo crear un administrador."
        )


#Comprobación de usuario y perfil.

@app.cli.command("ver-admin")
def ver_admin():

    # Buscamos usuario registrado.
    usuario = Usuario.query.first()

    # ¿Existe?
    if usuario is None:
        click.echo("No hay administradores registrados.")
        return

    # Buscamos perfil relacionado.
    perfil = Perfil.query.filter_by(
        usuario_id=usuario.id
    ).first()

    print("\nADMINISTRADOR DEL PORTFOLIO.")

    print("ID:", usuario.id)
    print("Usuario:", usuario.username)

    if perfil:

        print("Nombre:", perfil.nombre)
        print("Titulo:", perfil.titulo)
        print("ID del perfil:", perfil.id)

    else:
        print("El usuario no tiene un perfil asociado.")


# ------------------------------------
#Inicio de sesión.

@app.route("/login", methods=["GET", "POST"])
def login():

    # Si el usuario ya inició sesión,
    # lo redirigimos al portfolio.
    if current_user.is_authenticated:

        return redirect(url_for("index"))

    # Creamos una instancia del formulario.
    form = LoginForm()

    # Comprobamos que el formulario haya sido enviado
    # correctamente y que su token CSRF sea válido.
    if form.validate_on_submit():

        # Buscamos el usuario en MySQL.
        usuario = Usuario.query.filter_by(

            username=form.username.data.strip()

        ).first()

        # Comprobamos que el usuario exista
        # y que la contraseña coincida con su hash.
        if usuario and usuario.verificar_password(
            form.password.data
        ):

            # Iniciamos la sesión del administrador.
            login_user(usuario)

            # Mostramos un mensaje de confirmación.
            flash(
                "Sesión iniciada. Modo edición activado.",
                "success"
            )

            # Regresamos a la página principal.
            return redirect(url_for("index"))

        # Utilizamos un mensaje genérico para no revelar
        # si un determinado usuario existe o no.
        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    # Mostramos la plantilla de inicio de sesión.
    return render_template(
        "login.html",
        form=form
    )

# -----------------------------------------
#Cierre de sesión.

@app.route("/logout", methods=["POST"])
@login_required
def logout():

    # Comprobamos el formulario y su token CSRF.
    form = AccionForm()

    if not form.validate_on_submit():

        abort(400)

    # Finalizamos la sesión del administrador.
    logout_user()

    # Informamos al usuario.
    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    # Volvemos al portfolio público.
    return redirect(url_for("index"))

# -------------------------------------------
#Panel de prueba.

@app.route("/panel")
@login_required
def panel():

    # Solo registrados pueden acceder a esta ruta.

    return {
        "estado": "Acceso autorizado",
        "usuario": current_user.username,
        "modo": "Administrador"
    }


# ==========================================
# FUNCIONES AUXILIARES DEL CRUD
# ==========================================

def actualizar_datos(registro, form):

    # Recorremos los campos definidos
    # por nuestros formularios Flask-WTF.

    for campo in form:

        # Excluimos los campos que no pertenecen
        # a las columnas de MySQL.

        if campo.name in ("csrf_token", "submit"):
            continue

        valor = campo.data

        # Limpiamos espacios innecesarios.
        if isinstance(valor, str):

            valor = valor.strip()

            # Los campos opcionales vacíos
            # se almacenarán como NULL.
            if valor == "":
                valor = None

        # Actualizamos el atributo correspondiente.
        setattr(registro, campo.name, valor)


def guardar_cambios():

    try:

        # Confirmamos la transacción en MySQL.
        db.session.commit()

        return True

    except SQLAlchemyError:

        # Revertimos los cambios si ocurre un error.
        db.session.rollback()

        flash(
            "No se pudieron guardar los cambios.",
            "danger"
        )

        return False


def finalizar_edicion(ancla):

    # Si estamos utilizando una ventana modal,
    # mostramos una página de confirmación especial.
    if request.args.get("modal") == "1":

        return redirect(
            url_for(
                "edicion_completa",
                seccion=ancla
            )
        )

    # Si el formulario se abrió directamente,
    # regresamos al portfolio.
    return redirect(
        url_for("index", _anchor=ancla)
    )

# ==========================================
# EDITAR PERFIL PERSONAL
# ==========================================

@app.route(
    "/perfil/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_perfil():

    # Buscamos únicamente el perfil perteneciente
    # al usuario que inició sesión.
    perfil = Perfil.query.filter_by(
        usuario_id=current_user.id
    ).first_or_404()

    # obj=perfil carga automáticamente los datos
    # actuales de MySQL dentro del formulario.
    form = PerfilForm(obj=perfil)

    # Procesamos el formulario cuando se envía.
    if form.validate_on_submit():

        actualizar_datos(perfil, form)

        if guardar_cambios():

            flash(
                "Perfil actualizado correctamente.",
                "success"
            )

            return finalizar_edicion("acerca")

    # Mostramos el formulario de edición.
    return render_template(

        "formulario.html",

        form=form,

        titulo="Editar perfil personal",

        ancla="acerca"

    )


# ==========================================
# CREATE: AGREGAR CONTENIDO
# ==========================================

@app.route(
    "/<seccion>/agregar",
    methods=["GET", "POST"]
)
@login_required
def agregar(seccion):

    # Comprobamos que la sección solicitada exista.
    if seccion not in SECCIONES:

        abort(404)

    # Recuperamos la configuración correspondiente.
    modelo, formulario, nombre, ancla = SECCIONES[seccion]

    # Creamos el formulario vacío.
    form = formulario()

    if form.validate_on_submit():

        # Creamos un nuevo objeto del modelo.
        registro = modelo()

        # Asignamos los datos ingresados.
        actualizar_datos(registro, form)

        # Vinculamos el registro al administrador.
        registro.usuario_id = current_user.id

        # Agregamos el objeto a SQLAlchemy.
        db.session.add(registro)

        # Guardamos el registro en MySQL.
        if guardar_cambios():

            flash(
                "Elemento agregado correctamente.",
                "success"
            )

            return finalizar_edicion(ancla)

    return render_template(

        "formulario.html",

        form=form,

        titulo=f"Agregar {nombre}",

        ancla=ancla

    )

# ==========================================
# UPDATE: MODIFICAR CONTENIDO
# ==========================================

@app.route(
    "/<seccion>/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(seccion, id):

    # Validamos la sección solicitada.
    if seccion not in SECCIONES:

        abort(404)

    modelo, formulario, nombre, ancla = SECCIONES[seccion]

    # Buscamos el registro por su clave primaria
    # y comprobamos que pertenezca al usuario actual.
    registro = modelo.query.filter_by(

        id=id,

        usuario_id=current_user.id

    ).first_or_404()

    # Cargamos los datos existentes en el formulario.
    form = formulario(obj=registro)

    if form.validate_on_submit():

        actualizar_datos(registro, form)

        if guardar_cambios():

            flash(
                "Elemento actualizado correctamente.",
                "success"
            )

            return finalizar_edicion(ancla)

    return render_template(

        "formulario.html",

        form=form,

        titulo=f"Editar {nombre}",

        ancla=ancla

    )


# ==========================================
# DELETE: ELIMINAR CONTENIDO
# ==========================================

@app.route(
    "/<seccion>/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar(seccion, id):

    if seccion not in SECCIONES:

        abort(404)

    # Validamos el token CSRF.
    form = AccionForm()

    if not form.validate_on_submit():

        abort(400)

    modelo, formulario, nombre, ancla = SECCIONES[seccion]

    # Buscamos solamente registros pertenecientes
    # al administrador autenticado.
    registro = modelo.query.filter_by(

        id=id,

        usuario_id=current_user.id

    ).first_or_404()

    # Marcamos el registro para su eliminación.
    db.session.delete(registro)

    if guardar_cambios():

        flash(
            "Elemento eliminado correctamente.",
            "success"
        )

    return redirect(
        url_for("index", _anchor=ancla)
    )

# Confirmación de edición.

@app.route("/edicion/completa")
@login_required
def edicion_completa():

    # Recuperamos la sección que fue modificada.
    seccion = request.args.get("seccion", "acerca")

    # Solamente aceptamos identificadores conocidos.
    permitidas = {
        "acerca",
        "experiencia",
        "educacion",
        "habilidades",
        "proyectos"
    }

    if seccion not in permitidas:

        seccion = "acerca"

    return render_template(

        "edicion_completa.html",

        destino=url_for(
            "index",
            _anchor=seccion
        )

    )

# Descarga CV.

@app.route("/cv")
def descargar_cv():

    # Enviamos el PDF como archivo descargable.
    return send_from_directory(

        Path(app.static_folder) / "docs",

        "cv.pdf",

        as_attachment=True

    )


#Ejecución servidor.

if __name__ == "__main__":

    app.run()