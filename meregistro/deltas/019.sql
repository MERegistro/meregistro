BEGIN;

ALTER TABLE registro_anexo ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexo ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexo ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexo_conexion_internet ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexo_conexion_internet ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexo_conexion_internet ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexo_domicilio ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexo_domicilio ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexo_domicilio ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexo_edificio_compartido_niveles ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexo_edificio_compartido_niveles ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexo_edificio_compartido_niveles ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexo_informacion_edilicia ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexo_informacion_edilicia ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexo_informacion_edilicia ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexos_funciones ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexos_funciones ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexos_funciones ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexos_niveles ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexos_niveles ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexos_niveles ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_anexos_turnos ADD COLUMN last_user_id integer;
ALTER TABLE registro_anexos_turnos ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_anexos_turnos ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_autoridad_cargo ADD COLUMN last_user_id integer;
ALTER TABLE registro_autoridad_cargo ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_autoridad_cargo ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_dependencia_funcional ADD COLUMN last_user_id integer;
ALTER TABLE registro_dependencia_funcional ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_dependencia_funcional ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento_autoridades ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento_autoridades ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento_autoridades ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento_conexion_internet ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento_conexion_internet ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento_conexion_internet ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento_domicilio ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento_domicilio ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento_domicilio ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento_edificio_compartido_niveles ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento_edificio_compartido_niveles ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento_edificio_compartido_niveles ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimiento_informacion_edilicia ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimiento_informacion_edilicia ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimiento_informacion_edilicia ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimientos_funciones ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimientos_funciones ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimientos_funciones ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimientos_niveles ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimientos_niveles ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimientos_niveles ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_establecimientos_turnos ADD COLUMN last_user_id integer;
ALTER TABLE registro_establecimientos_turnos ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_establecimientos_turnos ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_estado_anexo ADD COLUMN last_user_id integer;
ALTER TABLE registro_estado_anexo ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_estado_anexo ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_estado_establecimiento ADD COLUMN last_user_id integer;
ALTER TABLE registro_estado_establecimiento ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_estado_establecimiento ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_estado_extension_aulica ADD COLUMN last_user_id integer;
ALTER TABLE registro_estado_extension_aulica ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_estado_extension_aulica ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_extension_aulica ADD COLUMN last_user_id integer;
ALTER TABLE registro_extension_aulica ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_extension_aulica ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_extension_aulica_domicilio ADD COLUMN last_user_id integer;
ALTER TABLE registro_extension_aulica_domicilio ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_extension_aulica_domicilio ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_extension_aulica_estados ADD COLUMN last_user_id integer;
ALTER TABLE registro_extension_aulica_estados ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_extension_aulica_estados ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_extensiones_aulicas_turnos ADD COLUMN last_user_id integer;
ALTER TABLE registro_extensiones_aulicas_turnos ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_extensiones_aulicas_turnos ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE registro_registro_establecimiento ADD COLUMN last_user_id integer;
ALTER TABLE registro_registro_establecimiento ADD COLUMN created_at timestamp without time zone;
ALTER TABLE registro_registro_establecimiento ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE seguridad_bloqueo_log ADD COLUMN last_user_id integer;
ALTER TABLE seguridad_bloqueo_log ADD COLUMN created_at timestamp without time zone;
ALTER TABLE seguridad_bloqueo_log ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE seguridad_perfil ADD COLUMN last_user_id integer;
ALTER TABLE seguridad_perfil ADD COLUMN created_at timestamp without time zone;
ALTER TABLE seguridad_perfil ADD COLUMN updated_at timestamp without time zone;

ALTER TABLE seguridad_usuario ADD COLUMN last_user_id integer;
ALTER TABLE seguridad_usuario ADD COLUMN created_at timestamp without time zone;
ALTER TABLE seguridad_usuario ADD COLUMN updated_at timestamp without time zone;


DROP TABLE IF EXISTS registro_anexo_version;
CREATE TABLE registro_anexo_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  cue character varying(2) NOT NULL ,
  fecha_alta date ,
  nombre character varying(255) NOT NULL ,
  telefono character varying(100) ,
  email character varying(255) ,
  sitio_web character varying(255) ,
  estado_id integer NOT NULL ,
  ambito_id integer ,
  old_id integer ,

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
  old_id ,

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
NEW.old_id,


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
  old_id ,

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
OLD.old_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_del();


DROP TABLE IF EXISTS registro_anexo_conexion_internet_version;
CREATE TABLE registro_anexo_conexion_internet_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  tipo_conexion_id integer NOT NULL ,
  proveedor character varying(30) NOT NULL ,
  tiene_conexion boolean NOT NULL ,
  costo numeric(122) NOT NULL ,
  cantidad integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_conexion_internet_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexo_conexion_internet()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_conexion_internet_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_conexion_internet_version(

  id ,
  anexo_id ,
  tipo_conexion_id ,
  proveedor ,
  tiene_conexion ,
  costo ,
  cantidad ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexo_id,
NEW.tipo_conexion_id,
NEW.proveedor,
NEW.tiene_conexion,
NEW.costo,
NEW.cantidad,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo_conexion_internet;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_conexion_internet
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_conexion_internet();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_conexion_internet_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_conexion_internet_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_conexion_internet_version(

  id ,
  anexo_id ,
  tipo_conexion_id ,
  proveedor ,
  tiene_conexion ,
  costo ,
  cantidad ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexo_id,
OLD.tipo_conexion_id,
OLD.proveedor,
OLD.tiene_conexion,
OLD.costo,
OLD.cantidad,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_conexion_internet;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo_conexion_internet
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_conexion_internet_del();


DROP TABLE IF EXISTS registro_anexo_domicilio_version;
CREATE TABLE registro_anexo_domicilio_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  tipo_domicilio_id integer NOT NULL ,
  localidad_id integer NOT NULL ,
  calle character varying(100) NOT NULL ,
  altura character varying(5) NOT NULL ,
  referencia character varying(255) ,
  cp character varying(20) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_domicilio_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexo_domicilio()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_domicilio_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_domicilio_version(

  id ,
  anexo_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexo_id,
NEW.tipo_domicilio_id,
NEW.localidad_id,
NEW.calle,
NEW.altura,
NEW.referencia,
NEW.cp,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo_domicilio;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_domicilio();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_domicilio_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_domicilio_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_domicilio_version(

  id ,
  anexo_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexo_id,
OLD.tipo_domicilio_id,
OLD.localidad_id,
OLD.calle,
OLD.altura,
OLD.referencia,
OLD.cp,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_domicilio;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_domicilio_del();


DROP TABLE IF EXISTS registro_anexo_edificio_compartido_niveles_version;
CREATE TABLE registro_anexo_edificio_compartido_niveles_version
(

  id integer NOT NULL ,
  anexoinformacionedilicia_id integer NOT NULL ,
  nivel_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_edificio_compartido_niveles_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexo_edificio_compartido_niveles()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_edificio_compartido_niveles_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_edificio_compartido_niveles_version(

  id ,
  anexoinformacionedilicia_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexoinformacionedilicia_id,
NEW.nivel_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexo_edificio_compartido_niveles;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_edificio_compartido_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_edificio_compartido_niveles();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_edificio_compartido_niveles_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_edificio_compartido_niveles_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_edificio_compartido_niveles_version(

  id ,
  anexoinformacionedilicia_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexoinformacionedilicia_id,
OLD.nivel_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_edificio_compartido_niveles;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo_edificio_compartido_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_edificio_compartido_niveles_del();


DROP TABLE IF EXISTS registro_anexo_informacion_edilicia_version;
CREATE TABLE registro_anexo_informacion_edilicia_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  tipo_dominio_id integer ,
  tipo_compartido_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexo_informacion_edilicia_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexo_informacion_edilicia()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_informacion_edilicia_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexo_informacion_edilicia_version(

  id ,
  anexo_id ,
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

DROP TRIGGER IF EXISTS auditar ON registro_anexo_informacion_edilicia;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo_informacion_edilicia
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_informacion_edilicia();


CREATE OR REPLACE FUNCTION auditar_registro_anexo_informacion_edilicia_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_informacion_edilicia_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_informacion_edilicia_version(

  id ,
  anexo_id ,
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
OLD.tipo_dominio_id,
OLD.tipo_compartido_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexo_informacion_edilicia;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexo_informacion_edilicia
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_informacion_edilicia_del();


DROP TABLE IF EXISTS registro_anexos_funciones_version;
CREATE TABLE registro_anexos_funciones_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  funcion_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexos_funciones_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexos_funciones()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_funciones_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexos_funciones_version(

  id ,
  anexo_id ,
  funcion_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexo_id,
NEW.funcion_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexos_funciones;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexos_funciones
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_funciones();


CREATE OR REPLACE FUNCTION auditar_registro_anexos_funciones_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_funciones_version
WHERE id = OLD.id;

INSERT INTO registro_anexos_funciones_version(

  id ,
  anexo_id ,
  funcion_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexo_id,
OLD.funcion_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexos_funciones;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexos_funciones
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_funciones_del();


DROP TABLE IF EXISTS registro_anexos_niveles_version;
CREATE TABLE registro_anexos_niveles_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  nivel_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexos_niveles_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexos_niveles()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_niveles_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexos_niveles_version(

  id ,
  anexo_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.anexo_id,
NEW.nivel_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexos_niveles;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexos_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_niveles();


CREATE OR REPLACE FUNCTION auditar_registro_anexos_niveles_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_niveles_version
WHERE id = OLD.id;

INSERT INTO registro_anexos_niveles_version(

  id ,
  anexo_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.anexo_id,
OLD.nivel_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexos_niveles;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexos_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_niveles_del();


DROP TABLE IF EXISTS registro_anexos_turnos_version;
CREATE TABLE registro_anexos_turnos_version
(

  id integer NOT NULL ,
  anexo_id integer NOT NULL ,
  turno_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_anexos_turnos_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_anexos_turnos()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_turnos_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_anexos_turnos_version(

  id ,
  anexo_id ,
  turno_id ,

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


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_anexos_turnos;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexos_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_turnos();


CREATE OR REPLACE FUNCTION auditar_registro_anexos_turnos_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexos_turnos_version
WHERE id = OLD.id;

INSERT INTO registro_anexos_turnos_version(

  id ,
  anexo_id ,
  turno_id ,

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


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_anexos_turnos;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_anexos_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexos_turnos_del();


DROP TABLE IF EXISTS registro_autoridad_cargo_version;
CREATE TABLE registro_autoridad_cargo_version
(

  id integer NOT NULL ,
  descripcion character varying(50) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_autoridad_cargo_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_autoridad_cargo()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_autoridad_cargo_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_autoridad_cargo_version(

  id ,
  descripcion ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.descripcion,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_autoridad_cargo;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_autoridad_cargo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_autoridad_cargo();


CREATE OR REPLACE FUNCTION auditar_registro_autoridad_cargo_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_autoridad_cargo_version
WHERE id = OLD.id;

INSERT INTO registro_autoridad_cargo_version(

  id ,
  descripcion ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.descripcion,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_autoridad_cargo;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_autoridad_cargo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_autoridad_cargo_del();


DROP TABLE IF EXISTS registro_dependencia_funcional_version;
CREATE TABLE registro_dependencia_funcional_version
(

  id integer NOT NULL ,
  nombre character varying(255) NOT NULL ,
  jurisdiccion_id integer NOT NULL ,
  tipo_gestion_id integer NOT NULL ,
  tipo_dependencia_funcional_id integer NOT NULL ,
  ambito_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_dependencia_funcional_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_dependencia_funcional()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_dependencia_funcional_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_dependencia_funcional_version(

  id ,
  nombre ,
  jurisdiccion_id ,
  tipo_gestion_id ,
  tipo_dependencia_funcional_id ,
  ambito_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.nombre,
NEW.jurisdiccion_id,
NEW.tipo_gestion_id,
NEW.tipo_dependencia_funcional_id,
NEW.ambito_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_dependencia_funcional;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_dependencia_funcional
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_dependencia_funcional();


CREATE OR REPLACE FUNCTION auditar_registro_dependencia_funcional_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_dependencia_funcional_version
WHERE id = OLD.id;

INSERT INTO registro_dependencia_funcional_version(

  id ,
  nombre ,
  jurisdiccion_id ,
  tipo_gestion_id ,
  tipo_dependencia_funcional_id ,
  ambito_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.nombre,
OLD.jurisdiccion_id,
OLD.tipo_gestion_id,
OLD.tipo_dependencia_funcional_id,
OLD.ambito_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_dependencia_funcional;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_dependencia_funcional
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_dependencia_funcional_del();


DROP TABLE IF EXISTS registro_establecimiento_version;
CREATE TABLE registro_establecimiento_version
(

  id integer NOT NULL ,
  dependencia_funcional_id integer NOT NULL ,
  cue character varying(9) NOT NULL ,
  nombre character varying(255) NOT NULL ,
  tipo_normativa_id integer NOT NULL ,
  unidad_academica boolean NOT NULL ,
  nombre_unidad_academica character varying(100) ,
  norma_creacion character varying(100) NOT NULL ,
  observaciones text ,
  anio_creacion integer ,
  telefono character varying(100) ,
  email character varying(255) ,
  sitio_web character varying(255) ,
  ambito_id integer ,
  estado_id integer ,
  old_id integer ,
  identificacion_provincial character varying(100) DEFAULT ''::character varying NOT NULL ,
  posee_subsidio boolean ,
  fax character varying(100) ,

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
  old_id ,
  identificacion_provincial ,
  posee_subsidio ,
  fax ,

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
NEW.old_id,
NEW.identificacion_provincial,
NEW.posee_subsidio,
NEW.fax,


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
  old_id ,
  identificacion_provincial ,
  posee_subsidio ,
  fax ,

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
OLD.old_id,
OLD.identificacion_provincial,
OLD.posee_subsidio,
OLD.fax,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_del();


DROP TABLE IF EXISTS registro_establecimiento_autoridades_version;
CREATE TABLE registro_establecimiento_autoridades_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  apellido character varying(40) NOT NULL ,
  nombre character varying(40) NOT NULL ,
  fecha_nacimiento date ,
  cargo_id integer ,
  tipo_documento_id integer ,
  documento character varying(20) ,
  telefono character varying(30) ,
  celular character varying(30) ,
  email character varying(255) ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_autoridades_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_autoridades()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_autoridades_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_autoridades_version(

  id ,
  establecimiento_id ,
  apellido ,
  nombre ,
  fecha_nacimiento ,
  cargo_id ,
  tipo_documento_id ,
  documento ,
  telefono ,
  celular ,
  email ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
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

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_autoridades;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_autoridades
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_autoridades();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_autoridades_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_autoridades_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_autoridades_version(

  id ,
  establecimiento_id ,
  apellido ,
  nombre ,
  fecha_nacimiento ,
  cargo_id ,
  tipo_documento_id ,
  documento ,
  telefono ,
  celular ,
  email ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
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

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_autoridades;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_autoridades
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_autoridades_del();


DROP TABLE IF EXISTS registro_establecimiento_conexion_internet_version;
CREATE TABLE registro_establecimiento_conexion_internet_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  tipo_conexion_id integer NOT NULL ,
  proveedor character varying(30) NOT NULL ,
  tiene_conexion boolean NOT NULL ,
  costo numeric(122) NOT NULL ,
  cantidad integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_conexion_internet_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_conexion_internet()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_conexion_internet_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_conexion_internet_version(

  id ,
  establecimiento_id ,
  tipo_conexion_id ,
  proveedor ,
  tiene_conexion ,
  costo ,
  cantidad ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.tipo_conexion_id,
NEW.proveedor,
NEW.tiene_conexion,
NEW.costo,
NEW.cantidad,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_conexion_internet;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_conexion_internet
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_conexion_internet();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_conexion_internet_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_conexion_internet_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_conexion_internet_version(

  id ,
  establecimiento_id ,
  tipo_conexion_id ,
  proveedor ,
  tiene_conexion ,
  costo ,
  cantidad ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.tipo_conexion_id,
OLD.proveedor,
OLD.tiene_conexion,
OLD.costo,
OLD.cantidad,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_conexion_internet;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_conexion_internet
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_conexion_internet_del();


DROP TABLE IF EXISTS registro_establecimiento_domicilio_version;
CREATE TABLE registro_establecimiento_domicilio_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  tipo_domicilio_id integer NOT NULL ,
  localidad_id integer NOT NULL ,
  calle character varying(100) NOT NULL ,
  altura character varying(5) NOT NULL ,
  referencia character varying(255) ,
  cp character varying(20) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_domicilio_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_domicilio()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_domicilio_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_domicilio_version(

  id ,
  establecimiento_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.tipo_domicilio_id,
NEW.localidad_id,
NEW.calle,
NEW.altura,
NEW.referencia,
NEW.cp,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_domicilio;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_domicilio();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_domicilio_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_domicilio_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_domicilio_version(

  id ,
  establecimiento_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.tipo_domicilio_id,
OLD.localidad_id,
OLD.calle,
OLD.altura,
OLD.referencia,
OLD.cp,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_domicilio;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_domicilio_del();


DROP TABLE IF EXISTS registro_establecimiento_edificio_compartido_niveles_version;
CREATE TABLE registro_establecimiento_edificio_compartido_niveles_version
(

  id integer NOT NULL ,
  establecimientoinformacionedilicia_id integer NOT NULL ,
  nivel_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_edificio_compartido_niveles_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_edificio_compartido_niveles()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_edificio_compartido_niveles_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_edificio_compartido_niveles_version(

  id ,
  establecimientoinformacionedilicia_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimientoinformacionedilicia_id,
NEW.nivel_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_edificio_compartido_niveles;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_edificio_compartido_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_edificio_compartido_niveles();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_edificio_compartido_niveles_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_edificio_compartido_niveles_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_edificio_compartido_niveles_version(

  id ,
  establecimientoinformacionedilicia_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimientoinformacionedilicia_id,
OLD.nivel_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_edificio_compartido_niveles;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_edificio_compartido_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_edificio_compartido_niveles_del();


DROP TABLE IF EXISTS registro_establecimiento_informacion_edilicia_version;
CREATE TABLE registro_establecimiento_informacion_edilicia_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  tipo_dominio_id integer ,
  tipo_compartido_id integer ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimiento_informacion_edilicia_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_informacion_edilicia()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_informacion_edilicia_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimiento_informacion_edilicia_version(

  id ,
  establecimiento_id ,
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

DROP TRIGGER IF EXISTS auditar ON registro_establecimiento_informacion_edilicia;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimiento_informacion_edilicia
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_informacion_edilicia();


CREATE OR REPLACE FUNCTION auditar_registro_establecimiento_informacion_edilicia_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimiento_informacion_edilicia_version
WHERE id = OLD.id;

INSERT INTO registro_establecimiento_informacion_edilicia_version(

  id ,
  establecimiento_id ,
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
OLD.tipo_dominio_id,
OLD.tipo_compartido_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento_informacion_edilicia;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimiento_informacion_edilicia
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_informacion_edilicia_del();


DROP TABLE IF EXISTS registro_establecimientos_funciones_version;
CREATE TABLE registro_establecimientos_funciones_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  funcion_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimientos_funciones_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_funciones()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_funciones_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimientos_funciones_version(

  id ,
  establecimiento_id ,
  funcion_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.funcion_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimientos_funciones;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimientos_funciones
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_funciones();


CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_funciones_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_funciones_version
WHERE id = OLD.id;

INSERT INTO registro_establecimientos_funciones_version(

  id ,
  establecimiento_id ,
  funcion_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.funcion_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimientos_funciones;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimientos_funciones
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_funciones_del();


DROP TABLE IF EXISTS registro_establecimientos_niveles_version;
CREATE TABLE registro_establecimientos_niveles_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  nivel_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimientos_niveles_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_niveles()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_niveles_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimientos_niveles_version(

  id ,
  establecimiento_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.nivel_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimientos_niveles;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimientos_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_niveles();


CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_niveles_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_niveles_version
WHERE id = OLD.id;

INSERT INTO registro_establecimientos_niveles_version(

  id ,
  establecimiento_id ,
  nivel_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.nivel_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimientos_niveles;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimientos_niveles
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_niveles_del();


DROP TABLE IF EXISTS registro_establecimientos_turnos_version;
CREATE TABLE registro_establecimientos_turnos_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  turno_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_establecimientos_turnos_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_turnos()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_turnos_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_establecimientos_turnos_version(

  id ,
  establecimiento_id ,
  turno_id ,

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


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_establecimientos_turnos;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_establecimientos_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_turnos();


CREATE OR REPLACE FUNCTION auditar_registro_establecimientos_turnos_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_establecimientos_turnos_version
WHERE id = OLD.id;

INSERT INTO registro_establecimientos_turnos_version(

  id ,
  establecimiento_id ,
  turno_id ,

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


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimientos_turnos;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_establecimientos_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimientos_turnos_del();


DROP TABLE IF EXISTS registro_estado_anexo_version;
CREATE TABLE registro_estado_anexo_version
(

  id integer NOT NULL ,
  nombre character varying(50) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_estado_anexo_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_estado_anexo()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_anexo_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_estado_anexo_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.nombre,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_estado_anexo;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_estado_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_anexo();


CREATE OR REPLACE FUNCTION auditar_registro_estado_anexo_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_anexo_version
WHERE id = OLD.id;

INSERT INTO registro_estado_anexo_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.nombre,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_estado_anexo;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_estado_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_anexo_del();


DROP TABLE IF EXISTS registro_estado_establecimiento_version;
CREATE TABLE registro_estado_establecimiento_version
(

  id integer NOT NULL ,
  nombre character varying(50) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_estado_establecimiento_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_estado_establecimiento()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_establecimiento_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_estado_establecimiento_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.nombre,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_estado_establecimiento;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_estado_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_establecimiento();


CREATE OR REPLACE FUNCTION auditar_registro_estado_establecimiento_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_establecimiento_version
WHERE id = OLD.id;

INSERT INTO registro_estado_establecimiento_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.nombre,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_estado_establecimiento;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_estado_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_establecimiento_del();


DROP TABLE IF EXISTS registro_estado_extension_aulica_version;
CREATE TABLE registro_estado_extension_aulica_version
(

  id integer NOT NULL ,
  nombre character varying(50) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_estado_extension_aulica_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_estado_extension_aulica()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_extension_aulica_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_estado_extension_aulica_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.nombre,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_estado_extension_aulica;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_estado_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_extension_aulica();


CREATE OR REPLACE FUNCTION auditar_registro_estado_extension_aulica_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_estado_extension_aulica_version
WHERE id = OLD.id;

INSERT INTO registro_estado_extension_aulica_version(

  id ,
  nombre ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.nombre,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_estado_extension_aulica;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_estado_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_estado_extension_aulica_del();


DROP TABLE IF EXISTS registro_extension_aulica_version;
CREATE TABLE registro_extension_aulica_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  nombre character varying(255) NOT NULL ,
  observaciones character varying(255) NOT NULL ,
  tipo_normativa_id integer NOT NULL ,
  fecha_alta date ,
  normativa character varying(100) NOT NULL ,
  anio_creacion integer ,
  sitio_web character varying(255) ,
  telefono character varying(100) ,
  email character varying(255) ,
  estado_id integer NOT NULL ,
  old_id integer ,

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
  old_id ,

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
NEW.old_id,


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
  old_id ,

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
OLD.old_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_del();


DROP TABLE IF EXISTS registro_extension_aulica_domicilio_version;
CREATE TABLE registro_extension_aulica_domicilio_version
(

  id integer NOT NULL ,
  extension_aulica_id integer NOT NULL ,
  tipo_domicilio_id integer NOT NULL ,
  localidad_id integer NOT NULL ,
  calle character varying(100) NOT NULL ,
  altura character varying(5) NOT NULL ,
  referencia character varying(255) ,
  cp character varying(20) NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_extension_aulica_domicilio_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_domicilio()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_domicilio_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_domicilio_version(

  id ,
  extension_aulica_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.extension_aulica_id,
NEW.tipo_domicilio_id,
NEW.localidad_id,
NEW.calle,
NEW.altura,
NEW.referencia,
NEW.cp,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica_domicilio;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_domicilio();


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_domicilio_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_domicilio_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_domicilio_version(

  id ,
  extension_aulica_id ,
  tipo_domicilio_id ,
  localidad_id ,
  calle ,
  altura ,
  referencia ,
  cp ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.extension_aulica_id,
OLD.tipo_domicilio_id,
OLD.localidad_id,
OLD.calle,
OLD.altura,
OLD.referencia,
OLD.cp,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica_domicilio;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extension_aulica_domicilio
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_domicilio_del();


DROP TABLE IF EXISTS registro_extension_aulica_estados_version;
CREATE TABLE registro_extension_aulica_estados_version
(

  id integer NOT NULL ,
  extension_aulica_id integer NOT NULL ,
  estado_id integer NOT NULL ,
  fecha date NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_extension_aulica_estados_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_estados()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_estados_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extension_aulica_estados_version(

  id ,
  extension_aulica_id ,
  estado_id ,
  fecha ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.extension_aulica_id,
NEW.estado_id,
NEW.fecha,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extension_aulica_estados;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extension_aulica_estados
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_estados();


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_estados_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_estados_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_estados_version(

  id ,
  extension_aulica_id ,
  estado_id ,
  fecha ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.extension_aulica_id,
OLD.estado_id,
OLD.fecha,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica_estados;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extension_aulica_estados
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_estados_del();


DROP TABLE IF EXISTS registro_extensiones_aulicas_turnos_version;
CREATE TABLE registro_extensiones_aulicas_turnos_version
(

  id integer NOT NULL ,
  extensionaulica_id integer NOT NULL ,
  turno_id integer NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_extensiones_aulicas_turnos_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_extensiones_aulicas_turnos()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extensiones_aulicas_turnos_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_extensiones_aulicas_turnos_version(

  id ,
  extensionaulica_id ,
  turno_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.extensionaulica_id,
NEW.turno_id,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_extensiones_aulicas_turnos;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_extensiones_aulicas_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extensiones_aulicas_turnos();


CREATE OR REPLACE FUNCTION auditar_registro_extensiones_aulicas_turnos_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extensiones_aulicas_turnos_version
WHERE id = OLD.id;

INSERT INTO registro_extensiones_aulicas_turnos_version(

  id ,
  extensionaulica_id ,
  turno_id ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.extensionaulica_id,
OLD.turno_id,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_extensiones_aulicas_turnos;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_extensiones_aulicas_turnos
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extensiones_aulicas_turnos_del();


DROP TABLE IF EXISTS registro_registro_establecimiento_version;
CREATE TABLE registro_registro_establecimiento_version
(

  id integer NOT NULL ,
  establecimiento_id integer NOT NULL ,
  estado_id integer NOT NULL ,
  fecha date NOT NULL ,
  observaciones text ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT registro_registro_establecimiento_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_registro_registro_establecimiento()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_registro_establecimiento_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO registro_registro_establecimiento_version(

  id ,
  establecimiento_id ,
  estado_id ,
  fecha ,
  observaciones ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.establecimiento_id,
NEW.estado_id,
NEW.fecha,
NEW.observaciones,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON registro_registro_establecimiento;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_registro_establecimiento();


CREATE OR REPLACE FUNCTION auditar_registro_registro_establecimiento_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_registro_establecimiento_version
WHERE id = OLD.id;

INSERT INTO registro_registro_establecimiento_version(

  id ,
  establecimiento_id ,
  estado_id ,
  fecha ,
  observaciones ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.establecimiento_id,
OLD.estado_id,
OLD.fecha,
OLD.observaciones,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_registro_establecimiento;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON registro_registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_registro_establecimiento_del();


DROP TABLE IF EXISTS seguridad_bloqueo_log_version;
CREATE TABLE seguridad_bloqueo_log_version
(

  id integer NOT NULL ,
  usuario_id integer NOT NULL ,
  motivo_id integer NOT NULL ,
  fecha date NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT seguridad_bloqueo_log_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_seguridad_bloqueo_log()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_bloqueo_log_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO seguridad_bloqueo_log_version(

  id ,
  usuario_id ,
  motivo_id ,
  fecha ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.usuario_id,
NEW.motivo_id,
NEW.fecha,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON seguridad_bloqueo_log;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON seguridad_bloqueo_log
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_bloqueo_log();


CREATE OR REPLACE FUNCTION auditar_seguridad_bloqueo_log_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_bloqueo_log_version
WHERE id = OLD.id;

INSERT INTO seguridad_bloqueo_log_version(

  id ,
  usuario_id ,
  motivo_id ,
  fecha ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.usuario_id,
OLD.motivo_id,
OLD.fecha,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON seguridad_bloqueo_log;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON seguridad_bloqueo_log
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_bloqueo_log_del();


DROP TABLE IF EXISTS seguridad_perfil_version;
CREATE TABLE seguridad_perfil_version
(

  id integer NOT NULL ,
  usuario_id integer NOT NULL ,
  ambito_id integer NOT NULL ,
  rol_id integer NOT NULL ,
  fecha_asignacion date NOT NULL ,
  fecha_desasignacion date ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT seguridad_perfil_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_seguridad_perfil()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_perfil_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO seguridad_perfil_version(

  id ,
  usuario_id ,
  ambito_id ,
  rol_id ,
  fecha_asignacion ,
  fecha_desasignacion ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.usuario_id,
NEW.ambito_id,
NEW.rol_id,
NEW.fecha_asignacion,
NEW.fecha_desasignacion,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON seguridad_perfil;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON seguridad_perfil
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_perfil();


CREATE OR REPLACE FUNCTION auditar_seguridad_perfil_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_perfil_version
WHERE id = OLD.id;

INSERT INTO seguridad_perfil_version(

  id ,
  usuario_id ,
  ambito_id ,
  rol_id ,
  fecha_asignacion ,
  fecha_desasignacion ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.usuario_id,
OLD.ambito_id,
OLD.rol_id,
OLD.fecha_asignacion,
OLD.fecha_desasignacion,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON seguridad_perfil;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON seguridad_perfil
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_perfil_del();


DROP TABLE IF EXISTS seguridad_usuario_version;
CREATE TABLE seguridad_usuario_version
(

  id integer NOT NULL ,
  tipo_documento_id integer NOT NULL ,
  documento character varying(20) NOT NULL ,
  apellido character varying(40) NOT NULL ,
  nombre character varying(40) NOT NULL ,
  email character varying(255) NOT NULL ,
  password character varying(255) ,
  last_login integer ,
  is_active boolean NOT NULL ,

  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT seguridad_usuario_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);



CREATE OR REPLACE FUNCTION auditar_seguridad_usuario()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_usuario_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO seguridad_usuario_version(

  id ,
  tipo_documento_id ,
  documento ,
  apellido ,
  nombre ,
  email ,
  password ,
  last_login ,
  is_active ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

NEW.id,
NEW.tipo_documento_id,
NEW.documento,
NEW.apellido,
NEW.nombre,
NEW.email,
NEW.password,
NEW.last_login,
NEW.is_active,


  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON seguridad_usuario;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON seguridad_usuario
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_usuario();


CREATE OR REPLACE FUNCTION auditar_seguridad_usuario_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_usuario_version
WHERE id = OLD.id;

INSERT INTO seguridad_usuario_version(

  id ,
  tipo_documento_id ,
  documento ,
  apellido ,
  nombre ,
  email ,
  password ,
  last_login ,
  is_active ,

  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (

OLD.id,
OLD.tipo_documento_id,
OLD.documento,
OLD.apellido,
OLD.nombre,
OLD.email,
OLD.password,
OLD.last_login,
OLD.is_active,


  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON seguridad_usuario;

CREATE TRIGGER auditar_del
BEFORE DELETE
ON seguridad_usuario
FOR EACH ROW
EXECUTE PROCEDURE auditar_seguridad_usuario_del();


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('019', 'Seguridad', 'Auditoria');

COMMIT;
