BEGIN;

DROP TABLE IF EXISTS registro_anexo_turno_version;
CREATE TABLE registro_anexo_turno_version
(

  id serial NOT NULL ,
  anexo_id integer NOT NULL ,
  turno_id integer NOT NULL ,
  tipo_dominio_id integer ,
  tipo_compartido_id integer ,
  last_user_id integer ,
  created_at timestamp without time zone ,
  updated_at timestamp without time zone ,

  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_turno_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_anexo_turno()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_turno_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_turno_version(

  id ,
  anexo_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexo_id,
NEW.turno_id,
NEW.tipo_dominio_id,
NEW.tipo_compartido_id,

  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo_turno;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_turno();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_turno_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_turno_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_turno_version(

  id ,
  anexo_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexo_id,
OLD.turno_id,
OLD.tipo_dominio_id,
OLD.tipo_compartido_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_turno;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_turno_del();


DROP TABLE IF EXISTS registro_establecimiento_turno_version;
CREATE TABLE registro_establecimiento_turno_version
(

  id serial NOT NULL ,
  establecimiento_id integer NOT NULL ,
  turno_id integer NOT NULL ,
  tipo_dominio_id integer ,
  tipo_compartido_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_turno_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_turno()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_turno_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_turno_version(

  id ,
  establecimiento_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.turno_id,
NEW.tipo_dominio_id,
NEW.tipo_compartido_id,

  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_turno;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_turno();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_turno_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_turno_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_turno_version(

  id ,
  establecimiento_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.turno_id,
OLD.tipo_dominio_id,
OLD.tipo_compartido_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_turno;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_turno_del();


DROP TABLE IF EXISTS registro_extension_aulica_turno_version;
CREATE TABLE registro_extension_aulica_turno_version
(

  id serial NOT NULL ,
  extension_aulica_id integer NOT NULL ,
  turno_id integer NOT NULL ,
  tipo_dominio_id integer ,
  tipo_compartido_id integer ,
  last_user_id integer ,
  created_at timestamp without time zone ,
  updated_at timestamp without time zone ,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_extension_aulica_turno_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_turno()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_turno_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_turno_version(

  id ,
  extension_aulica_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.extension_aulica_id,
NEW.turno_id,
NEW.tipo_dominio_id,
NEW.tipo_compartido_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica_turno;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_turno();


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_turno_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_turno_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_turno_version(

  id ,
  extension_aulica_id ,
  turno_id ,
  tipo_dominio_id ,
  tipo_compartido_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.extension_aulica_id,
OLD.turno_id,
OLD.tipo_dominio_id,
OLD.tipo_compartido_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica_turno;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extension_aulica_turno
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_turno_del();

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('076', 'Registro', 'Ticket #219');

COMMIT;
