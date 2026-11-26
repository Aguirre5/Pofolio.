import click

from flask import Flask

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

#-----------------------------------------
#Ruta principal Portfolio.

@app.route("/")
def index():

    # Buscamos perfil.
    perfil = Perfil.query.order_by(
        Perfil.id
    ).first()

    # ¿Existe?
    if perfil is None:

        return "Portfolio sin inicializar.", 503

    # Devolvemos información.
    # Flask convierte el diccionario a JSON.
    return {

        "proyecto": "P. Portfolio.",

        "nombre": perfil.nombre,

        "titulo": perfil.titulo,

        "descripcion": perfil.descripcion

    }






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

# ==========================================
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

#Ejecución servidor.

if __name__ == "__main__":

    app.run()