-- Proyecto P. Portfolio.
-- Diseno fisico db MySQL.

CREATE TABLE IF NOT EXISTS usuarios (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS educacion (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	titulo VARCHAR(150) NOT NULL, 
	institucion VARCHAR(150), 
	periodo VARCHAR(100), 
	descripcion TEXT, 
	imagen VARCHAR(500), 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS experiencias (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	puesto VARCHAR(150) NOT NULL, 
	empresa VARCHAR(150), 
	periodo VARCHAR(100), 
	descripcion TEXT, 
	imagen VARCHAR(500), 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS habilidades (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	nombre VARCHAR(150) NOT NULL, 
	tipo VARCHAR(30) NOT NULL, 
	porcentaje INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT check_porcentaje CHECK (porcentaje >= 0 AND porcentaje <= 100), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS perfil (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	titulo VARCHAR(150), 
	descripcion TEXT, 
	ubicacion VARCHAR(150), 
	email VARCHAR(150), 
	github VARCHAR(500), 
	linkedin VARCHAR(500), 
	foto VARCHAR(500), 
	banner VARCHAR(500), 
	PRIMARY KEY (id), 
	UNIQUE (usuario_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS proyectos (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	nombre VARCHAR(150) NOT NULL, 
	fecha VARCHAR(100), 
	descripcion TEXT, 
	enlace VARCHAR(500), 
	imagen VARCHAR(500), 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

-- Usuario posee perfil y habilidades.
-- Usuario registra experiencias y educación.
-- Usuario desarrolla proyectos.

-- Fin diseño fisico db from my MySQL.