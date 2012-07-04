BEGIN;

-- Table: registro_establecimiento_matricula
-- DROP TABLE registro_establecimiento_matricula;
CREATE TABLE registro_establecimiento_matricula
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_establecimiento_matricula_pkey PRIMARY KEY (id),
  CONSTRAINT registro_establecimiento_matricula_establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_matricula_establecimiento_id_anio_key UNIQUE (establecimiento_id, anio),
  CONSTRAINT registro_establecimiento_matricula_formacion_continua_check CHECK (formacion_continua >= 0),
  CONSTRAINT registro_establecimiento_matricula_formacion_docente_check CHECK (formacion_docente >= 0),
  CONSTRAINT registro_establecimiento_matricula_postitulos_check CHECK (postitulos >= 0),
  CONSTRAINT registro_establecimiento_matricula_profesorados_check CHECK (profesorados >= 0),
  CONSTRAINT registro_establecimiento_matricula_tecnicaturas_check CHECK (tecnicaturas >= 0),
  CONSTRAINT registro_establecimiento_matricula_total_check CHECK (total >= 0)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_establecimiento_matricula_establecimiento_id
-- DROP INDEX registro_establecimiento_matricula_establecimiento_id;
CREATE INDEX registro_establecimiento_matricula_establecimiento_id
  ON registro_establecimiento_matricula
  USING btree
  (establecimiento_id);

-- Table: registro_establecimiento_matricula_version
-- DROP TABLE registro_establecimiento_matricula_version;
CREATE TABLE registro_establecimiento_matricula_version
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  deleted boolean,
  "version" bigint NOT NULL,
  CONSTRAINT registro_establecimiento_matricula_version_pkey PRIMARY KEY (id, version)
)
WITH (
  OIDS=FALSE
);

-- Table: registro_anexo_matricula
-- DROP TABLE registro_anexo_matricula;
CREATE TABLE registro_anexo_matricula
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_anexo_matricula_pkey PRIMARY KEY (id),
  CONSTRAINT registro_anexo_matricula_anexo_id_fkey FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_matricula_anexo_id_anio_key UNIQUE (anexo_id, anio),
  CONSTRAINT registro_anexo_matricula_formacion_continua_check CHECK (formacion_continua >= 0),
  CONSTRAINT registro_anexo_matricula_formacion_docente_check CHECK (formacion_docente >= 0),
  CONSTRAINT registro_anexo_matricula_postitulos_check CHECK (postitulos >= 0),
  CONSTRAINT registro_anexo_matricula_profesorados_check CHECK (profesorados >= 0),
  CONSTRAINT registro_anexo_matricula_tecnicaturas_check CHECK (tecnicaturas >= 0),
  CONSTRAINT registro_anexo_matricula_total_check CHECK (total >= 0)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_anexo_matricula_anexo_id
-- DROP INDEX registro_anexo_matricula_anexo_id;
CREATE INDEX registro_anexo_matricula_anexo_id
  ON registro_anexo_matricula
  USING btree
  (anexo_id);

-- Table: registro_anexo_matricula_version
-- DROP TABLE registro_anexo_matricula_version;
CREATE TABLE registro_anexo_matricula_version
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  deleted boolean,
  "version" bigint NOT NULL,
  CONSTRAINT registro_anexo_matricula_version_pkey PRIMARY KEY (id, version)
)
WITH (
  OIDS=FALSE
);


-- Table: registro_extension_aulica_matricula
-- DROP TABLE registro_extension_aulica_matricula;
CREATE TABLE registro_extension_aulica_matricula
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_extension_aulica_matricula_pkey PRIMARY KEY (id),
  CONSTRAINT registro_extension_aulica_matricula_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_matricul_extension_aulica_id_anio_key UNIQUE (extension_aulica_id, anio),
  CONSTRAINT registro_extension_aulica_matricula_formacion_continua_check CHECK (formacion_continua >= 0),
  CONSTRAINT registro_extension_aulica_matricula_formacion_docente_check CHECK (formacion_docente >= 0),
  CONSTRAINT registro_extension_aulica_matricula_postitulos_check CHECK (postitulos >= 0),
  CONSTRAINT registro_extension_aulica_matricula_profesorados_check CHECK (profesorados >= 0),
  CONSTRAINT registro_extension_aulica_matricula_tecnicaturas_check CHECK (tecnicaturas >= 0),
  CONSTRAINT registro_extension_aulica_matricula_total_check CHECK (total >= 0)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_extension_aulica_matricula_extension_aulica_id
-- DROP INDEX registro_extension_aulica_matricula_extension_aulica_id;
CREATE INDEX registro_extension_aulica_matricula_extension_aulica_id
  ON registro_extension_aulica_matricula
  USING btree
  (extension_aulica_id);

-- Table: registro_extension_aulica_matricula_version
-- DROP TABLE registro_extension_aulica_matricula_version;
CREATE TABLE registro_extension_aulica_matricula_version
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  anio integer NOT NULL,
  mixto boolean,
  profesorados integer,
  postitulos integer,
  formacion_docente integer,
  formacion_continua integer,
  tecnicaturas integer,
  total integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  deleted boolean,
  "version" bigint NOT NULL,
  CONSTRAINT registro_extension_aulica_matricula_version_pkey PRIMARY KEY (id, version)
)
WITH (
  OIDS=FALSE
);

--
--

ALTER TABLE registro_establecimiento_verificacion_datos ADD COLUMN matricula boolean;
ALTER TABLE registro_anexo_verificacion_datos ADD COLUMN matricula boolean;
ALTER TABLE registro_extension_aulica_verificacion_datos ADD COLUMN matricula boolean;

UPDATE registro_establecimiento_verificacion_datos SET matricula = False;
UPDATE registro_anexo_verificacion_datos SET matricula = False;
UPDATE registro_extension_aulica_verificacion_datos SET matricula = False;

ALTER TABLE registro_establecimiento_verificacion_datos ALTER COLUMN matricula SET NOT NULL;
ALTER TABLE registro_anexo_verificacion_datos ALTER COLUMN matricula SET NOT NULL;
ALTER TABLE registro_extension_aulica_verificacion_datos ALTER COLUMN matricula SET NOT NULL;

--
--
--
-- AUDITAR
--
--

CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_matricula()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_matricula_version
WHERE id = NEW.id;
IF (vers = 1) THEN
	NEW.created_at = NOW();
	NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_matricula_version(
    id,
    establecimiento_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (
    NEW.id,
    NEW.establecimiento_id,
    NEW.anio,
    NEW.mixto,
    NEW.profesorados,
    NEW.postitulos,
    NEW.formacion_docente,
    NEW.formacion_continua,
    NEW.tecnicaturas,
    NEW.total,

	NEW.last_user_id,
	CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
	NOW(),
	vers,
	FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_matricula;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_matricula();

-- Delete

CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_matricula_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_matricula_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_matricula_version(
    id,
    establecimiento_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
)
VALUES (
    OLD.id,
    OLD.establecimiento_id,
    OLD.anio,
    OLD.mixto,
    OLD.profesorados,
    OLD.postitulos,
    OLD.formacion_docente,
    OLD.formacion_continua,
    OLD.tecnicaturas,
    OLD.total,

	OLD.last_user_id,
	CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
	NOW(),
	vers,
	TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_matricula;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_establecimiento_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_matricula_del();

--
--

CREATE OR REPLACE FUNCTION auditar_registro_anexo_matricula()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_matricula_version
WHERE id = NEW.id;
IF (vers = 1) THEN
	NEW.created_at = NOW();
	NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_matricula_version(
    id,
    anexo_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (
    NEW.id,
    NEW.anexo_id,
    NEW.anio,
    NEW.mixto,
    NEW.profesorados,
    NEW.postitulos,
    NEW.formacion_docente,
    NEW.formacion_continua,
    NEW.tecnicaturas,
    NEW.total,

	NEW.last_user_id,
	CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
	NOW(),
	vers,
	FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo_matricula;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_matricula();

-- Delete

CREATE OR REPLACE FUNCTION auditar_registro_anexo_matricula_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_matricula_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_matricula_version(
    id,
    anexo_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
)
VALUES (
    OLD.id,
    OLD.anexo_id,
    OLD.anio,
    OLD.mixto,
    OLD.profesorados,
    OLD.postitulos,
    OLD.formacion_docente,
    OLD.formacion_continua,
    OLD.tecnicaturas,
    OLD.total,

	OLD.last_user_id,
	CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
	NOW(),
	vers,
	TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_matricula;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_anexo_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_matricula_del();

--
--

CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_matricula()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_matricula_version
WHERE id = NEW.id;
IF (vers = 1) THEN
	NEW.created_at = NOW();
	NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_matricula_version(
    id,
    extension_aulica_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (
    NEW.id,
    NEW.extension_aulica_id,
    NEW.anio,
    NEW.mixto,
    NEW.profesorados,
    NEW.postitulos,
    NEW.formacion_docente,
    NEW.formacion_continua,
    NEW.tecnicaturas,
    NEW.total,

	NEW.last_user_id,
	CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
	NOW(),
	vers,
	FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica_matricula;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_matricula();

-- Delete

CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_matricula_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_matricula_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_matricula_version(
    id,
    extension_aulica_id,
    anio,
    mixto,
    profesorados,
    postitulos,
    formacion_docente,
    formacion_continua,
    tecnicaturas,
    total,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
)
VALUES (
    OLD.id,
    OLD.extension_aulica_id,
    OLD.anio,
    OLD.mixto,
    OLD.profesorados,
    OLD.postitulos,
    OLD.formacion_docente,
    OLD.formacion_continua,
    OLD.tecnicaturas,
    OLD.total,

	OLD.last_user_id,
	CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
	NOW(),
	vers,
	TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica_matricula;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_extension_aulica_matricula
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_matricula_del();

--
--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('075', 'Registro', 'Matrícula - Ticket #220');

COMMIT;
