BEGIN;

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('registro_certificar_carga', 'Certificar carga de datos de establecimientos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Registro'), 'Registro');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'registro_certificar_carga')
);

-------------------------------------

--
-- Table: registro_establecimiento_certificacion_carga
-- DROP TABLE registro_establecimiento_certificacion_carga;
CREATE TABLE registro_establecimiento_certificacion_carga
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  anio integer NOT NULL,
  fecha date NOT NULL,
  usuario_id integer NOT NULL,
  CONSTRAINT registro_establecimiento_certificacion_carga_pkey PRIMARY KEY (id),
  CONSTRAINT registro_establecimiento_certificacion__establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_certificacion_carga_usuario_id_fkey FOREIGN KEY (usuario_id)
      REFERENCES seguridad_usuario (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_certificacion_c_establecimiento_id_key UNIQUE (establecimiento_id, anio)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE registro_establecimiento_certificacion_carga
  OWNER TO postgres;

-- Index: registro_establecimiento_certificacion_carga_establecimiento_id
-- DROP INDEX registro_establecimiento_certificacion_carga_establecimiento_id;
CREATE INDEX registro_establecimiento_certificacion_carga_establecimiento_id
  ON registro_establecimiento_certificacion_carga
  USING btree
  (establecimiento_id);

-- Index: registro_establecimiento_certificacion_carga_usuario_id
-- DROP INDEX registro_establecimiento_certificacion_carga_usuario_id;
CREATE INDEX registro_establecimiento_certificacion_carga_usuario_id
  ON registro_establecimiento_certificacion_carga
  USING btree
  (usuario_id);


-- Table: registro_anexo_certificacion_carga
-- DROP TABLE registro_anexo_certificacion_carga;
CREATE TABLE registro_anexo_certificacion_carga
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  anio integer NOT NULL,
  fecha date NOT NULL,
  usuario_id integer NOT NULL,
  CONSTRAINT registro_anexo_certificacion_carga_pkey PRIMARY KEY (id),
  CONSTRAINT registro_anexo_certificacion_carga_anexo_id_fkey FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_certificacion_carga_usuario_id_fkey FOREIGN KEY (usuario_id)
      REFERENCES seguridad_usuario (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_certificacion_carga_anexo_id_key UNIQUE (anexo_id, anio)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE registro_anexo_certificacion_carga
  OWNER TO postgres;

-- Index: registro_anexo_certificacion_carga_anexo_id
-- DROP INDEX registro_anexo_certificacion_carga_anexo_id;
CREATE INDEX registro_anexo_certificacion_carga_anexo_id
  ON registro_anexo_certificacion_carga
  USING btree
  (anexo_id);

-- Index: registro_anexo_certificacion_carga_usuario_id
-- DROP INDEX registro_anexo_certificacion_carga_usuario_id;
CREATE INDEX registro_anexo_certificacion_carga_usuario_id
  ON registro_anexo_certificacion_carga
  USING btree
  (usuario_id);

-- Table: registro_extension_aulica_certificacion_carga
-- DROP TABLE registro_extension_aulica_certificacion_carga;
CREATE TABLE registro_extension_aulica_certificacion_carga
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  anio integer NOT NULL,
  fecha date NOT NULL,
  usuario_id integer NOT NULL,
  CONSTRAINT registro_extension_aulica_certificacion_carga_pkey PRIMARY KEY (id),
  CONSTRAINT registro_extension_aulica_certificacio_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_certificacion_carga_usuario_id_fkey FOREIGN KEY (usuario_id)
      REFERENCES seguridad_usuario (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_certificacion_extension_aulica_id_key UNIQUE (extension_aulica_id, anio)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE registro_extension_aulica_certificacion_carga
  OWNER TO postgres;

-- Index: registro_extension_aulica_certificacion_carga_extension_aulica_
-- DROP INDEX registro_extension_aulica_certificacion_carga_extension_aulica_;
CREATE INDEX registro_extension_aulica_certificacion_carga_extension_aulica_
  ON registro_extension_aulica_certificacion_carga
  USING btree
  (extension_aulica_id);

-- Index: registro_extension_aulica_certificacion_carga_usuario_id
-- DROP INDEX registro_extension_aulica_certificacion_carga_usuario_id;
CREATE INDEX registro_extension_aulica_certificacion_carga_usuario_id
  ON registro_extension_aulica_certificacion_carga
  USING btree
  (usuario_id);



---------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('143', 'Registro', '#459');

COMMIT;
