BEGIN;

ALTER TABLE seguridad_configuracion_solapas_extension_aulica ADD COLUMN autoridades BOOLEAN;
UPDATE seguridad_configuracion_solapas_extension_aulica SET autoridades = TRUE;
ALTER TABLE seguridad_configuracion_solapas_extension_aulica ALTER COLUMN autoridades SET NOT NULL;

-- Table: registro_extension_aulica_autoridades

-- DROP TABLE registro_extension_aulica_autoridades;

CREATE TABLE registro_extension_aulica_autoridades
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  apellido character varying(40) NOT NULL,
  nombre character varying(40) NOT NULL,
  fecha_nacimiento date,
  cargo_id integer,
  tipo_documento_id integer,
  documento character varying(20),
  telefono character varying(30),
  celular character varying(30),
  email character varying(255),
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_extension_aulica_autoridades_pkey PRIMARY KEY (id ),
  CONSTRAINT registro_extension_aulica_autoridades_cargo_id_fkey FOREIGN KEY (cargo_id)
      REFERENCES registro_autoridad_cargo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_autoridades_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_autoridades_tipo_documento_id_fkey FOREIGN KEY (tipo_documento_id)
      REFERENCES seguridad_tipo_documento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

ALTER TABLE registro_extension_aulica_verificacion_datos ADD COLUMN "autoridades" boolean NOT NULL DEFAULT false;

--
--
--

DROP TABLE IF EXISTS registro_extension_aulica_autoridades_version;
CREATE TABLE registro_extension_aulica_autoridades_version (
	id integer NOT NULL,
	extension_aulica_id integer NOT NULL,
	apellido character varying(40) NOT NULL,
	nombre character varying(40) NOT NULL,
	fecha_nacimiento date,
	cargo_id integer,
	tipo_documento_id integer,
	documento character varying(20),
	telefono character varying(30),
	celular character varying(30),
	email character varying(255),

	last_user_id integer,
	created_at timestamp without time zone,
	updated_at timestamp without time zone,
	"version" bigint NOT NULL,
	deleted boolean,
	CONSTRAINT registro_extension_aulica_autoridades_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_autoridades()
RETURNS "trigger" AS $$
DECLARE
	vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_autoridades_version
WHERE id = NEW.id;

IF (vers = 1) THEN
	NEW.created_at = NOW();
	NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_autoridades_version(
	id,
	extension_aulica_id,
	apellido,
	nombre,
	fecha_nacimiento,
	cargo_id,
	tipo_documento_id,
	documento,
	telefono,
	celular,
	email,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (

	NEW.id,
	NEW.extension_aulica_id,
	NEW.apellido,
	NEW.nombre,
	NEW.fecha_nacimiento,
	NEW.cargo_id,
	NEW.tipo_documento_id,
	NEW.documento,
	NEW.telefono,
	NEW.celular,
	NEW.email,

	NEW.last_user_id,
	CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
	NOW(),
	vers,
	FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica_autoridades;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica_autoridades
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_autoridades();


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_autoridades_del()
RETURNS "trigger" AS $$
DECLARE
	vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_autoridades_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_autoridades_version(
	id,
	extension_aulica_id,
	apellido,
	nombre,
	fecha_nacimiento,
	cargo_id,
	tipo_documento_id,
	documento,
	telefono,
	celular,
	email,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (
	OLD.id,
	OLD.extension_aulica_id,
	OLD.apellido,
	OLD.nombre,
	OLD.fecha_nacimiento,
	OLD.cargo_id,
	OLD.tipo_documento_id,
	OLD.documento,
	OLD.telefono,
	OLD.celular,
	OLD.email,

	OLD.last_user_id,
	CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
	NOW(),
	vers,
	TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica_autoridades;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_extension_aulica_autoridades
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_autoridades_del();


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('085', 'Registro', 'Ticket #270');

COMMIT;
