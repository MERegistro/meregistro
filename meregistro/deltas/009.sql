-- Autoridad del establecimiento - Ticket #71
BEGIN;
--
-- DROP TABLE registro_tipo_autoridad;

CREATE TABLE registro_autoridad_cargo (
  id serial NOT NULL,
  descripcion character varying(50) NOT NULL,
  CONSTRAINT registro_autoridad_cargo_pkey PRIMARY KEY (id),
  CONSTRAINT registro_autoridad_cargo_descripcion_key UNIQUE (descripcion)
)
WITH (
  OIDS=FALSE
);
INSERT INTO registro_autoridad_cargo (id, descripcion) VALUES (1, 'Rector/Director');
---------------------------------------
-- DROP TABLE registro_establecimiento_autoridades;

CREATE TABLE registro_establecimiento_autoridades
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  apellido character varying(40) NOT NULL,
  nombre character varying(40) NOT NULL,
  fecha_nacimiento date,
  cargo_id integer,
  tipo_documento_id integer,
  documento character varying(20),
  telefono character varying(30),
  celular character varying(30),
  email character varying(255),
  CONSTRAINT registro_establecimiento_autoridades_pkey PRIMARY KEY (id),
  CONSTRAINT registro_establecimiento_autoridades_establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_autoridades_cargo_id_fkey FOREIGN KEY (cargo_id)
      REFERENCES registro_autoridad_cargo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_autoridades_tipo_documento_id_fkey FOREIGN KEY (tipo_documento_id)
      REFERENCES seguridad_tipo_documento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
---------------------------------------
--
--
-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reg_establecimiento_autoridad_consulta', 'Consulta de autoridades del establecimiento', 2);
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reg_establecimiento_autoridad_create', 'Alta nueva autoridad del establecimiento', 2);
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reg_establecimiento_autoridad_edit', 'Edición de datos de autoridad del establecimiento', 2);
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reg_establecimiento_autoridad_delete', 'Eliminación de datos de autoridad del establecimiento', 2);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'RectorDirectorIFD'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_consulta')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'RectorDirectorIFD'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_create')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'RectorDirectorIFD'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_edit')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'RectorDirectorIFD'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_delete')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_consulta')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminTitulos'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_autoridad_consulta')
);
---------------------------------------
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('009', 'Registro', 'Autoridades del establecimiento - Ticket #71');

--
COMMIT;
