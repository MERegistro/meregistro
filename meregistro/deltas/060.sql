BEGIN;

-- Vuelven los niveles a lo que corresponde
UPDATE registro_nivel
SET nombre = 'Inicial'
WHERE nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Inicial';
UPDATE registro_nivel
SET nombre = 'Primaria'
WHERE nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Primaria';
UPDATE registro_nivel
SET nombre = 'Secundaria'
WHERE nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Secundaria';
UPDATE registro_nivel
SET nombre = 'Superior'
WHERE nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Superior';

--
-- Creo la tabla de alcance
CREATE TABLE registro_alcance
(
  id serial NOT NULL,
  nombre character varying(100) NOT NULL,
  CONSTRAINT registro_alcance_pkey PRIMARY KEY (id),
  CONSTRAINT registro_alcance_nombre_key UNIQUE (nombre)
)
WITH (
  OIDS=FALSE
);
INSERT INTO registro_alcance (nombre) VALUES
('Oferta Carreras que Habilitan para Ejercer en la Educación Inicial'),
('Oferta Carreras que Habilitan para Ejercer en la Educación Primaria'),
('Oferta Carreras que Habilitan para Ejercer en la Educación Secundaria'),
('Oferta Carreras que Habilitan para Ejercer en la Educación Superior');

--
--
-- Cambio las tablas de verificación
ALTER TABLE registro_establecimiento_verificacion_datos RENAME COLUMN niveles TO alcances;
ALTER TABLE registro_anexo_verificacion_datos RENAME COLUMN niveles TO alcances;
ALTER TABLE registro_extension_aulica_verificacion_datos RENAME COLUMN niveles TO alcances;
--
--
-- Las nuevas tablas de alcances
DROP TABLE
registro_establecimientos_niveles, registro_establecimientos_niveles_version,
registro_anexos_niveles, registro_anexos_niveles_version,
registro_extension_aulica_niveles;

--
CREATE TABLE registro_establecimientos_alcances
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  alcance_id integer NOT NULL,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_establecimientos_alcances_pkey PRIMARY KEY (id),
  CONSTRAINT establecimiento_id_refs_id_6ac8c760 FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimientos_alcances_alcance_id_fkey FOREIGN KEY (alcance_id)
      REFERENCES registro_alcance (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimientos_alcances_establecimiento_id_key UNIQUE (establecimiento_id, alcance_id)
)
WITH (
  OIDS=FALSE
);
--
CREATE TABLE registro_anexos_alcances
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  alcance_id integer NOT NULL,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_anexos_alcances_pkey PRIMARY KEY (id),
  CONSTRAINT anexo_id_refs_id_72fb65f8 FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexos_alcances_nivel_id_fkey FOREIGN KEY (alcance_id)
      REFERENCES registro_alcance (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexos_alcances_anexo_id_key UNIQUE (anexo_id, alcance_id)
)
WITH (
  OIDS=FALSE
);
--
CREATE TABLE registro_extension_aulica_alcances
(
  id serial NOT NULL,
  extensionaulica_id integer NOT NULL,
  alcance_id integer NOT NULL,
  CONSTRAINT registro_extension_aulica_alcances_pkey PRIMARY KEY (id),
  CONSTRAINT extensionaulica_id_refs_id_413a1592 FOREIGN KEY (extensionaulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_alcances_alcance_id_fkey FOREIGN KEY (alcance_id)
      REFERENCES registro_alcance (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_alcance_unique_key UNIQUE (extensionaulica_id, alcance_id)
)
WITH (
  OIDS=FALSE
);

--
--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('060', 'Registro', '#207 - Parte 2');

COMMIT;
