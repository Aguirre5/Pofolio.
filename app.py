from flask import Flask
# Trabajo con MySQL.
from flask_sqlalchemy import SQLAlchemy

# Consultas SQL.
from sqlalchemy import text

# config.
from config import Config

#Aplicación:

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

#Ruta principal Portfolio.

@app.route("/")
def index():
    
    return "Proyecto P. Portfolio."

#Conexión MYSQL prueba.
@app.cli.command("test-db")
def probar_base_datos():
    try:

        # Ejecutamos consulta sencilla.
        resultado = db.session.execute(
            text("SELECT 1")
        ).scalar()

        # Comprobamos MySQL correctamente.
        if resultado == 1:

            print("Conexion con MySQL exitosa.")

    except Exception as error:

        # Mostramos error local.
        print("Error de conexion:", error)

        raise SystemExit(1)

    finally:

        # Liberamos sesión de bd.
        db.session.remove()
        
        
#Ejecución servidor.

if __name__ == "__main__":

    app.run()