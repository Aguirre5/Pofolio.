from flask_sqlalchemy import SQLAlchemy

# Creadora de clases y métodos abstractos.
# ABC define clases abstractas.
# abstractmethod define métodos abstractos.
from abc import ABC, abstractmethod

# UserMixin para gestionar usuarios y sesiones.
from flask_login import UserMixin

# Gestionadoras de contraseñas.
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Instancia de SQLAlchemy.
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):

    # Nombre de tabla de MySQL.
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    # Atributo privado para encapsular hash.
    __password_hash = db.Column(
        "password_hash",
        db.String(255),
        nullable=False
    )
    # PSWD pasa por Werkzeug para generar hash seguro y lo almacena en MYSQL.

    # Dar contraseña.
    def establecer_password(self, password):

        self.__password_hash = generate_password_hash(
            password
        )

    # Comprob. contraseña.
    def verificar_password(self, password):

        return check_password_hash(
            self.__password_hash,
            password
        )

class Perfil(db.Model):

    __tablename__ = "perfil"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    # Información personal.
    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    titulo = db.Column(db.String(150))

    descripcion = db.Column(db.Text)

    ubicacion = db.Column(db.String(150))

    email = db.Column(db.String(150))

    # Enlaces a redes sociales.
    github = db.Column(db.String(500))

    linkedin = db.Column(db.String(500))

    # Direcciones imágenes.
    foto = db.Column(db.String(500))

    banner = db.Column(db.String(500))

class Experiencia(db.Model):

    __tablename__ = "experiencias"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # 1:M.
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    puesto = db.Column(
        db.String(150),
        nullable=False
    )

    empresa = db.Column(db.String(150))

    periodo = db.Column(db.String(100))

    descripcion = db.Column(db.Text)

    imagen = db.Column(db.String(500))

class Educacion(db.Model):

    __tablename__ = "educacion"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Relación 1:M.
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    institucion = db.Column(db.String(150))

    periodo = db.Column(db.String(100))

    descripcion = db.Column(db.Text)

    # Logo ITR.
    imagen = db.Column(db.String(500))

class Habilidad(db.Model):

    __tablename__ = "habilidades"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    # Nombre habilidad.
    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    # Tipo de habilidad: hard, soft o idioma.
    tipo = db.Column(
        db.String(30),
        nullable=False
    )

    # Nivel en porcentaje.
    porcentaje = db.Column(
        db.Integer,
        nullable=False
    )

    # Restricción porcentajes inválidos.
    __table_args__ = (
        db.CheckConstraint(
            "porcentaje >= 0 AND porcentaje <= 100",
            name="check_porcentaje"
        ),
    )

class Proyecto(db.Model):

    __tablename__ = "proyectos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    fecha = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    enlace = db.Column(db.String(500))
    imagen = db.Column(db.String(500))
    

# Abstracción:
# Esta clase representa el comportamiento general
# de los contenidos que aparecerán en el portfolio.

class Contenido(ABC):

    # Las clases definiran cómo obtener
    # título de cada contenido.

    @abstractmethod
    def obtener_titulo(self):
        pass

    # Las clases derivadas definiran cómo obtener
    # descripción de cada contenido.

    @abstractmethod
    def obtener_detalle(self):
        pass


# Herencia:
# Las siguientes clases heredan de Contenido
# e implementan métodos abstractos.

class TarjetaExperiencia(Contenido):

    def __init__(self, experiencia):
        self.experiencia = experiencia

    # Método abstracto.
    def obtener_titulo(self):
        return self.experiencia.puesto

    def obtener_detalle(self):
        return self.experiencia.empresa


class TarjetaEducacion(Contenido):

    def __init__(self, educacion):
        self.educacion = educacion

    def obtener_titulo(self):
        return self.educacion.titulo

    def obtener_detalle(self):
        return self.educacion.institucion


class TarjetaProyecto(Contenido):

    def __init__(self, proyecto):
        self.proyecto = proyecto

    def obtener_titulo(self):
        return self.proyecto.nombre

    def obtener_detalle(self):
        return self.proyecto.fecha
    


# Polimorfismo:

# Esta función puede recibir cualquier objeto
# perteneciente a una clase derivada de Contenido.
# Dependiendo del objeto recibido, los métodos
# tendrán un comportamiento diferente.

def presentar_contenido(contenido: Contenido):

    return {
        "titulo": contenido.obtener_titulo(),
        "detalle": contenido.obtener_detalle()
    }

""" 
En resumen, la clase de abstracción Contenido: 
Define estructura general de los contenidos del portqfolio.
Automatizando la obtención de títulos y detalles en conjunto
con a un comportamiento polimórfico de las clases derivadas.

Experiencia tendrá puesto y empresa.
Educación tendrá título e institución.
Proyecto tendrá nombre y fecha.
"""