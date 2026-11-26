# Acceso a variables de entorno.
import os

# Permite cargar las variables del archivo .env.
from dotenv import load_dotenv

# Cargamos las variables de entorno.
load_dotenv()

class Config:

    # Clave secreta utilizada para proteger sesiones.
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Obtenemos URL de conexión MySQL.
    DATABASE_URL = os.environ["DATABASE_URL"]

    # Adaptamos URL de Clever Cloud para PyMySQL.
    if DATABASE_URL.startswith("mysql://"):

        DATABASE_URL = DATABASE_URL.replace(
            "mysql://",
            "mysql+pymysql://",
            1
        )

    # Indicamos a SQLAlchemy dónde está nuestra base de datos.
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuramos conexiones MySQL.
    SQLALCHEMY_ENGINE_OPTIONS = {

        # Comprueba si la conexión continúa activa.
        "pool_pre_ping": True,

        # Renueva conexiones antiguas.
        "pool_recycle": 280,

        # Limita conexiones simultáneas.
        "pool_size": 2,

        "max_overflow": 2
    }

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # En Render, las cookies deberán utilizar HTTPS.
    SESSION_COOKIE_SECURE = (
        os.getenv("RENDER") == "true"
    )