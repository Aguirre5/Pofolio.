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
    Proyecto
)

#Aplicación:

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

#Ruta principal Portfolio.

@app.route("/")
def index():
    
    return "Proyecto P. Portfolio."

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
        "-- Diseno fisico db MySQL.",
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

    print("Diseno fisico exportado.")
    print("Archivo:", archivo)



#Ejecución servidor.

if __name__ == "__main__":

    app.run()