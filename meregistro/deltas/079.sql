BEGIN;

DROP TABLE IF EXISTS registro_anexo_version;
CREATE TABLE registro_anexo_version
(

  id serial NOT NULL ,
  establecimiento_id integer NOT NULL ,
  cue character varying(9) NOT NULL ,
  fecha_alta date ,
  nombre character varying(255) NOT NULL ,
  telefono character varying(100) ,
  email character varying(255) ,
  sitio_web character varying(255) ,
  estado_id integer NOT NULL ,
  ambito_id integer ,
  anio_creacion integer ,
  norma_creacion character varying(100) ,
  tipo_norma_otra character varying(100) ,
  observaciones character varying(255) ,
  fax character varying(100) ,
  interno character varying(10) ,
  tipo_norma_id integer ,
  tipo_normativa_id integer ,
  subsidio_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_anexo()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_version(

  id ,
  establecimiento_id ,
  cue ,
  fecha_alta ,
  nombre ,
  telefono ,
  email ,
  sitio_web ,
  estado_id ,
  ambito_id ,
  anio_creacion ,
  norma_creacion ,
  tipo_norma_otra ,
  observaciones ,
  fax ,
  interno ,
  tipo_norma_id ,
  tipo_normativa_id ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.cue,
NEW.fecha_alta,
NEW.nombre,
NEW.telefono,
NEW.email,
NEW.sitio_web,
NEW.estado_id,
NEW.ambito_id,
NEW.anio_creacion,
NEW.norma_creacion,
NEW.tipo_norma_otra,
NEW.observaciones,
NEW.fax,
NEW.interno,
NEW.tipo_norma_id,
NEW.tipo_normativa_id,
NEW.subsidio_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_version(

  id ,
  establecimiento_id ,
  cue ,
  fecha_alta ,
  nombre ,
  telefono ,
  email ,
  sitio_web ,
  estado_id ,
  ambito_id ,
  anio_creacion ,
  norma_creacion ,
  tipo_norma_otra ,
  observaciones ,
  fax ,
  interno ,
  tipo_norma_id ,
  tipo_normativa_id ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.cue,
OLD.fecha_alta,
OLD.nombre,
OLD.telefono,
OLD.email,
OLD.sitio_web,
OLD.estado_id,
OLD.ambito_id,
OLD.anio_creacion,
OLD.norma_creacion,
OLD.tipo_norma_otra,
OLD.observaciones,
OLD.fax,
OLD.interno,
OLD.tipo_norma_id,
OLD.tipo_normativa_id,
OLD.subsidio_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_del();


DROP TABLE IF EXISTS registro_establecimiento_version;
CREATE TABLE registro_establecimiento_version
(

  id serial NOT NULL ,
  dependencia_funcional_id integer NOT NULL ,
  cue character varying(9) NOT NULL ,
  nombre character varying(255) NOT NULL ,
  tipo_normativa_id integer ,
  unidad_academica boolean NOT NULL ,
  nombre_unidad_academica character varying(100) ,
  norma_creacion character varying(100) ,
  observaciones text ,
  anio_creacion integer ,
  telefono character varying(100) ,
  email character varying(255) ,
  sitio_web character varying(255) ,
  ambito_id integer ,
  estado_id integer ,
  fax character varying(100) ,
  solicitud_filename character varying(100) ,
  tipo_norma_id integer ,
  tipo_norma_otra character varying(100) ,
  interno character varying(10) ,
  subsidio_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_version(

  id ,
  dependencia_funcional_id ,
  cue ,
  nombre ,
  tipo_normativa_id ,
  unidad_academica ,
  nombre_unidad_academica ,
  norma_creacion ,
  observaciones ,
  anio_creacion ,
  telefono ,
  email ,
  sitio_web ,
  ambito_id ,
  estado_id ,
  fax ,
  solicitud_filename ,
  tipo_norma_id ,
  tipo_norma_otra ,
  interno ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.dependencia_funcional_id,
NEW.cue,
NEW.nombre,
NEW.tipo_normativa_id,
NEW.unidad_academica,
NEW.nombre_unidad_academica,
NEW.norma_creacion,
NEW.observaciones,
NEW.anio_creacion,
NEW.telefono,
NEW.email,
NEW.sitio_web,
NEW.ambito_id,
NEW.estado_id,
NEW.fax,
NEW.solicitud_filename,
NEW.tipo_norma_id,
NEW.tipo_norma_otra,
NEW.interno,
NEW.subsidio_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_version(

  id ,
  dependencia_funcional_id ,
  cue ,
  nombre ,
  tipo_normativa_id ,
  unidad_academica ,
  nombre_unidad_academica ,
  norma_creacion ,
  observaciones ,
  anio_creacion ,
  telefono ,
  email ,
  sitio_web ,
  ambito_id ,
  estado_id ,
  fax ,
  solicitud_filename ,
  tipo_norma_id ,
  tipo_norma_otra ,
  interno ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.dependencia_funcional_id,
OLD.cue,
OLD.nombre,
OLD.tipo_normativa_id,
OLD.unidad_academica,
OLD.nombre_unidad_academica,
OLD.norma_creacion,
OLD.observaciones,
OLD.anio_creacion,
OLD.telefono,
OLD.email,
OLD.sitio_web,
OLD.ambito_id,
OLD.estado_id,
OLD.fax,
OLD.solicitud_filename,
OLD.tipo_norma_id,
OLD.tipo_norma_otra,
OLD.interno,
OLD.subsidio_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_del();


DROP TABLE IF EXISTS registro_extension_aulica_version;
CREATE TABLE registro_extension_aulica_version
(

  id serial NOT NULL ,
  establecimiento_id integer NOT NULL ,
  nombre character varying(255) NOT NULL ,
  observaciones character varying(255) ,
  tipo_normativa_id integer ,
  fecha_alta date ,
  normativa character varying(100) ,
  anio_creacion integer ,
  sitio_web character varying(255) ,
  telefono character varying(100) ,
  email character varying(255) ,
  estado_id integer NOT NULL ,
  cue character varying(9) ,
  norma_creacion character varying(100) ,
  norma_creacion_otra character varying(100) ,
  norma_creacion_numero character varying(30) ,
  ambito_id integer ,
  origen_norma_id integer ,
  subsidio_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_extension_aulica_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_version(

  id ,
  establecimiento_id ,
  nombre ,
  observaciones ,
  tipo_normativa_id ,
  fecha_alta ,
  normativa ,
  anio_creacion ,
  sitio_web ,
  telefono ,
  email ,
  estado_id ,
  cue ,
  norma_creacion ,
  norma_creacion_otra ,
  norma_creacion_numero ,
  ambito_id ,
  origen_norma_id ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.nombre,
NEW.observaciones,
NEW.tipo_normativa_id,
NEW.fecha_alta,
NEW.normativa,
NEW.anio_creacion,
NEW.sitio_web,
NEW.telefono,
NEW.email,
NEW.estado_id,
NEW.cue,
NEW.norma_creacion,
NEW.norma_creacion_otra,
NEW.norma_creacion_numero,
NEW.ambito_id,
NEW.origen_norma_id,
NEW.subsidio_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica();


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_version(

  id ,
  establecimiento_id ,
  nombre ,
  observaciones ,
  tipo_normativa_id ,
  fecha_alta ,
  normativa ,
  anio_creacion ,
  sitio_web ,
  telefono ,
  email ,
  estado_id ,
  cue ,
  norma_creacion ,
  norma_creacion_otra ,
  norma_creacion_numero ,
  ambito_id ,
  origen_norma_id ,
  subsidio_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.nombre,
OLD.observaciones,
OLD.tipo_normativa_id,
OLD.fecha_alta,
OLD.normativa,
OLD.anio_creacion,
OLD.sitio_web,
OLD.telefono,
OLD.email,
OLD.estado_id,
OLD.cue,
OLD.norma_creacion,
OLD.norma_creacion_otra,
OLD.norma_creacion_numero,
OLD.ambito_id,
OLD.origen_norma_id,
OLD.subsidio_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_del();

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('079', 'Registro', 'Ticket #234');


COMMIT;