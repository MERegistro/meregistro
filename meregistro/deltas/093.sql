BEGIN;

-------------------------------------
-- Table: titulos_estado_titulo_nacional

-- DROP TABLE titulos_estado_titulo_nacional;

CREATE TABLE titulos_estado_titulo_nacional
(
  id serial NOT NULL,
  nombre character varying(50) NOT NULL,
  CONSTRAINT titulos_estado_titulo_nacional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_estado_titulo_nacional_nombre_key UNIQUE (nombre )
)
WITH (
  OIDS=FALSE
);

INSERT INTO titulos_estado_titulo_nacional (nombre) VALUES ('Vigente'), ('No vigente');

-------------------------------------
-- Table: titulos_titulo_nacional

-- DROP TABLE titulos_titulo_nacional;

CREATE TABLE titulos_titulo_nacional
(
  id serial NOT NULL,
  nombre character varying(200) NOT NULL,
  normativa_nacional_id integer NOT NULL,
  observaciones character varying(255),
  estado_id integer NOT NULL,
  fecha_alta date NOT NULL,
  CONSTRAINT titulos_titulo_nacional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_titulo_nacional_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_titulo_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_titulo_nacional_normativa_nacional_id_fkey FOREIGN KEY (normativa_nacional_id)
      REFERENCES titulos_normativa_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_titulo_nacional_nombre_normativa_nacional_id_key UNIQUE (nombre , normativa_nacional_id )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_titulo_nacional_estado_id

-- DROP INDEX titulos_titulo_nacional_estado_id;

CREATE INDEX titulos_titulo_nacional_estado_id
  ON titulos_titulo_nacional
  USING btree
  (estado_id );

-- Index: titulos_titulo_nacional_normativa_nacional_id

-- DROP INDEX titulos_titulo_nacional_normativa_nacional_id;

CREATE INDEX titulos_titulo_nacional_normativa_nacional_id
  ON titulos_titulo_nacional
  USING btree
  (normativa_nacional_id );

  
-------------------------------------
-- Table: titulos_titulo_nacional_estados

-- DROP TABLE titulos_titulo_nacional_estados;

CREATE TABLE titulos_titulo_nacional_estados
(
  id serial NOT NULL,
  titulo_nacional_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_titulo_nacional_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_titulo_nacional_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_titulo_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_titulo_nacional_estados_titulo_nacional_id_fkey FOREIGN KEY (titulo_nacional_id)
      REFERENCES titulos_titulo_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_titulo_nacional_estados_estado_id

-- DROP INDEX titulos_titulo_nacional_estados_estado_id;

CREATE INDEX titulos_titulo_nacional_estados_estado_id
  ON titulos_titulo_nacional_estados
  USING btree
  (estado_id );

-- Index: titulos_titulo_nacional_estados_titulo_nacional_id

-- DROP INDEX titulos_titulo_nacional_estados_titulo_nacional_id;

CREATE INDEX titulos_titulo_nacional_estados_titulo_nacional_id
  ON titulos_titulo_nacional_estados
  USING btree
  (titulo_nacional_id );


-------------------------------------

-- Table: titulos_titulos_nacionales_carreras

-- DROP TABLE titulos_titulos_nacionales_carreras;

CREATE TABLE titulos_titulos_nacionales_carreras
(
  id serial NOT NULL,
  titulonacional_id integer NOT NULL,
  carrera_id integer NOT NULL,
  CONSTRAINT titulos_titulos_nacionales_carreras_pkey PRIMARY KEY (id ),
  CONSTRAINT titulonacional_id_refs_id_e359564c FOREIGN KEY (titulonacional_id)
      REFERENCES titulos_titulo_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_titulos_nacionales_carreras_carrera_id_fkey FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_titulos_nacionales_car_titulonacional_id_carrera_id_key UNIQUE (titulonacional_id , carrera_id )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_titulos_nacionales_carreras_carrera_id

-- DROP INDEX titulos_titulos_nacionales_carreras_carrera_id;

CREATE INDEX titulos_titulos_nacionales_carreras_carrera_id
  ON titulos_titulos_nacionales_carreras
  USING btree
  (carrera_id );

-- Index: titulos_titulos_nacionales_carreras_titulonacional_id

-- DROP INDEX titulos_titulos_nacionales_carreras_titulonacional_id;

CREATE INDEX titulos_titulos_nacionales_carreras_titulonacional_id
  ON titulos_titulos_nacionales_carreras
  USING btree
  (titulonacional_id );


-------------------------------------
-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_titulo_nacional_consulta', 'Consultar Títulos Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_titulo_nacional_alta', 'Alta de Títulos Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_titulo_nacional_modificar', 'Modificar Títulos Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_titulo_nacional_baja', 'Eliminar Títulos Nacionales', 3, 'Títulos');


INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_consulta')
);
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_consulta')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_alta')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_modificar')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_nacional_baja')
);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('093', 'Titulos', 'Ticket #294');

COMMIT;
