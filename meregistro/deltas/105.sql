BEGIN;

--
--
-- Validez nacional

INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES ('Validez Nacional', 'Validez Nacional', '/validez_nacional/');

-- Table: validez_nacional_estado_solicitud

-- DROP TABLE validez_nacional_estado_solicitud;

CREATE TABLE validez_nacional_estado_solicitud
(
  id serial NOT NULL,
  nombre character varying(50) NOT NULL,
  CONSTRAINT validez_nacional_estado_solicitud_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_estado_solicitud_nombre_key UNIQUE (nombre)
)
WITH (
  OIDS=FALSE
);
INSERT INTO validez_nacional_estado_solicitud (nombre) VALUES ('Pendiente'), ('Controlado');

-------------------------------------

-- Table: validez_nacional_solicitud

-- DROP TABLE validez_nacional_solicitud;

CREATE TABLE validez_nacional_solicitud
(
  id serial NOT NULL,
  jurisdiccion_id integer NOT NULL,
  carrera_id integer NOT NULL,
  titulo_nacional_id integer NOT NULL,
  primera_cohorte integer,
  ultima_cohorte integer,
  dictamen_cofev character varying(200),
  normativas_nacionales character varying(99),
  estado_id integer NOT NULL,
  CONSTRAINT validez_nacional_solicitud_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_solicitud_carrera_id_fkey FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES validez_nacional_estado_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id)
      REFERENCES registro_jurisdiccion (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_titulo_nacional_id_fkey FOREIGN KEY (titulo_nacional_id)
      REFERENCES titulos_titulo_nacional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_primera_cohorte_check CHECK (primera_cohorte >= 0),
  CONSTRAINT validez_nacional_solicitud_ultima_cohorte_check CHECK (ultima_cohorte >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_solicitud_carrera_id
-- DROP INDEX validez_nacional_solicitud_carrera_id;
CREATE INDEX validez_nacional_solicitud_carrera_id
  ON validez_nacional_solicitud
  USING btree
  (carrera_id);

-- Index: validez_nacional_solicitud_estado_id
-- DROP INDEX validez_nacional_solicitud_estado_id;
CREATE INDEX validez_nacional_solicitud_estado_id
  ON validez_nacional_solicitud
  USING btree
  (estado_id);

-- Index: validez_nacional_solicitud_jurisdiccion_id
-- DROP INDEX validez_nacional_solicitud_jurisdiccion_id;
CREATE INDEX validez_nacional_solicitud_jurisdiccion_id
  ON validez_nacional_solicitud
  USING btree
  (jurisdiccion_id);

-- Index: validez_nacional_solicitud_titulo_nacional_id
-- DROP INDEX validez_nacional_solicitud_titulo_nacional_id;
CREATE INDEX validez_nacional_solicitud_titulo_nacional_id
  ON validez_nacional_solicitud
  USING btree
  (titulo_nacional_id);

-------------------------------------

-- Table: validez_nacional_solicitud_normativas

-- DROP TABLE validez_nacional_solicitud_normativas;

CREATE TABLE validez_nacional_solicitud_normativas_jurisdiccionales
(
  id serial NOT NULL,
  solicitud_id integer NOT NULL,
  normativajurisdiccional_id integer NOT NULL,
  CONSTRAINT validez_nacional_solicitud_normativas_pkey PRIMARY KEY (id),
  CONSTRAINT solicitud_id_refs_id_6bd66323 FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_norm_normativajurisdiccional_id_fkey FOREIGN KEY (normativajurisdiccional_id)
      REFERENCES titulos_normativa_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_no_solicitud_id_normativajurisdi_key UNIQUE (solicitud_id, normativajurisdiccional_id)
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_solicitud_normativas_normativajurisdicciondcde
-- DROP INDEX validez_nacional_solicitud_normativas_normativajurisdicciondcde;
CREATE INDEX validez_nacional_solicitud_normativas_normativajurisdicciondcde
  ON validez_nacional_solicitud_normativas
  USING btree
  (normativajurisdiccional_id);

-- Index: validez_nacional_solicitud_normativas_solicitud_id
-- DROP INDEX validez_nacional_solicitud_normativas_solicitud_id;
CREATE INDEX validez_nacional_solicitud_normativas_solicitud_id
  ON validez_nacional_solicitud_normativas
  USING btree
  (solicitud_id);
  
-------------------------------------
  
-- Table: validez_nacional_validez_nacional
-- DROP TABLE validez_nacional_validez_nacional;

CREATE TABLE validez_nacional_validez_nacional
(
  id serial NOT NULL,
  solicitud_id integer NOT NULL,
  nro_infd character varying(99) NOT NULL,
  cue character varying(9) NOT NULL,
  tipo_unidad_educativa character varying(10) NOT NULL,
  unidad_educativa_id integer NOT NULL,
  CONSTRAINT validez_nacional_validez_nacional_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_validez_nacional_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_validez_nacional_unidad_educativa_id_check CHECK (unidad_educativa_id >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_validez_nacional_cue
-- DROP INDEX validez_nacional_validez_nacional_cue;
CREATE INDEX validez_nacional_validez_nacional_cue
  ON validez_nacional_validez_nacional
  USING btree
  (cue);
-- Index: validez_nacional_validez_nacional_cue_like
-- DROP INDEX validez_nacional_validez_nacional_cue_like;
CREATE INDEX validez_nacional_validez_nacional_cue_like
  ON validez_nacional_validez_nacional
  USING btree
  (cue varchar_pattern_ops);
-- Index: validez_nacional_validez_nacional_solicitud_id
-- DROP INDEX validez_nacional_validez_nacional_solicitud_id;
CREATE INDEX validez_nacional_validez_nacional_solicitud_id
  ON validez_nacional_validez_nacional
  USING btree
  (solicitud_id);

-------------------------------------

-- Table: validez_nacional_solicitud_estados

-- DROP TABLE validez_nacional_solicitud_estados;

CREATE TABLE validez_nacional_solicitud_estados
(
  id serial NOT NULL,
  solicitud_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT validez_nacional_solicitud_estados_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_solicitud_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES validez_nacional_estado_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_estados_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_solicitud_estados_estado_id
-- DROP INDEX validez_nacional_solicitud_estados_estado_id;
CREATE INDEX validez_nacional_solicitud_estados_estado_id
  ON validez_nacional_solicitud_estados
  USING btree
  (estado_id);

-- Index: validez_nacional_solicitud_estados_solicitud_id
-- DROP INDEX validez_nacional_solicitud_estados_solicitud_id;
CREATE INDEX validez_nacional_solicitud_estados_solicitud_id
  ON validez_nacional_solicitud_estados
  USING btree
  (solicitud_id);

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
	('validez_nacional_solicitud', 'Solicitar Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
	('validez_nacional_control', 'Controlar solicitudes de Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud')
);
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_control')
);

-------------------------------------


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('105', 'Validez Nacional', 'Avances Ticket #322');

COMMIT;
