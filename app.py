from flask import Flask

app = Flask(__name__)

# RUTA PRINCIPAL DEL PORTFOLIO.
# El decorador route vincula una URL con una función de Python.

@app.route("/")
def index():

    # Retornamos el contenido que recibirá el navegador.
    return "Proyecto Integrador - Portfolio Full Stack"

# EJECUCIÓN SERVIDOR.
# El archivo se ejecuta directamente.

if __name__ == "__main__":

    app.run(debug=True)