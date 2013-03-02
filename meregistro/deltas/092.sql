BEGIN;

-------------------------------------
-- Table: titulos_estado_normativa_nacional

-- DROP TABLE titulos_estado_normativa_nacional;

CREATE TABLE titulos_estado_normativa_nacional
(
  id serial NOT NULL,
  nombre character varying(50) NOT NULL,
  CONSTRAINT titulos_estado_normativa_nacional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_estado_normativa_nacional_nombre_key UNIQUE (nombre )
)
WITH (
  OIDS=FALSE
);

INSERT INTO titulos_estado_normativa_nacional (nombre) VALUES ('Vigente'), ('No vigente');

-------------------------------------

-- Table: titulos_normativa_nacional

-- DROP TABLE titulos_normativa_nacional;

CREATE TABLE titulos_normativa_nacional
(
  id serial NOT NULL,
  numero character varying(50) NOT NULL,
  descripcion character varying(255) NOT NULL,
  observaciones character varying(255),
  estado_id integer NOT NULL,
  fecha_alta date NOT NULL,
  CONSTRAINT titulos_normativa_nacional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_normativa_nacional_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_normativa_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_normativa_nacional_numero_key UNIQUE (numero )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_normativa_nacional_estado_id

-- DROP INDEX titulos_normativa_nacional_estado_id;

CREATE INDEX titulos_normativa_nacional_estado_id
  ON titulos_normativa_nacional
  USING btree
  (estado_id );

-------------------------------------

-- Table: titulos_normativa_nacional_estados

-- DROP TABLE titulos_normativa_nacional_estados;

CREATE TABLE titulos_normativa_nacional_estados
(
  id serial NOT NULL,
  normativa_nacional_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_normativa_nacional_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_normativa_nacional_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_normativa_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_normativa_nacional_estados_normativa_nacional_id_fkey FOREIGN KEY (normativa_nacional_id)
      REFERENCES titulos_normativa_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_normativa_nacional_estados_estado_id

-- DROP INDEX titulos_normativa_nacional_estados_estado_id;

CREATE INDEX titulos_normativa_nacional_estados_estado_id
  ON titulos_normativa_nacional_estados
  USING btree
  (estado_id );

-- Index: titulos_normativa_nacional_estados_normativa_nacional_id

-- DROP INDEX titulos_normativa_nacional_estados_normativa_nacional_id;

CREATE INDEX titulos_normativa_nacional_estados_normativa_nacional_id
  ON titulos_normativa_nacional_estados
  USING btree
  (normativa_nacional_id );

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_normativa_nacional_consulta', 'Consultar Normativas Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_normativa_nacional_alta', 'Alta de Normativas Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_normativa_nacional_modificar', 'Modificar Normativas Nacionales', 3, 'Títulos');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_normativa_nacional_baja', 'Eliminar Normativas Nacionales', 3, 'Títulos');


INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_consulta')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('092', 'Titulos', 'Ticket #291');

COMMIT;
