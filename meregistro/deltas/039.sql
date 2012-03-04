-- Ticket #167

BEGIN;

-- Columnas

ALTER TABLE registro_anexo DROP COLUMN old_id;
ALTER TABLE registro_anexo_version DROP COLUMN old_id;

ALTER TABLE registro_establecimiento DROP COLUMN old_id;
ALTER TABLE registro_establecimiento_version DROP COLUMN old_id;

ALTER TABLE registro_extension_aulica DROP COLUMN old_id;
ALTER TABLE registro_extension_aulica_version DROP COLUMN old_id;

--

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
	id,
	dependencia_funcional_id,
	cue,
	nombre,
	tipo_normativa_id,
	unidad_academica,
	nombre_unidad_academica,
	norma_creacion,
	observaciones,
	anio_creacion,
	solicitud_filename,
	telefono,
	interno,
	email,
	sitio_web,
	ambito_id,
	estado_id,
	posee_subsidio,
	fax,

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
	NEW.solicitud_filename,
	NEW.telefono,
	NEW.interno,
	NEW.email,
	NEW.sitio_web,
	NEW.ambito_id,
	NEW.estado_id,
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
	id,
	dependencia_funcional_id,
	cue,
	nombre,
	tipo_normativa_id,
	unidad_academica,
	nombre_unidad_academica,
	norma_creacion,
	observaciones,
	anio_creacion,
	solicitud_filename,
	telefono,
	interno,
	email,
	sitio_web,
	ambito_id,
	estado_id,
	posee_subsidio,
	fax,

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
	OLD.solicitud_filename,
	OLD.telefono,
	OLD.interno,
	OLD.email,
	OLD.sitio_web,
	OLD.ambito_id,
	OLD.estado_id,
	OLD.posee_subsidio,
	OLD.fax,

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
AFTER DELETE
ON registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_del();

--
--
-- Nuevo audit de anexo

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
	id,
	establecimiento_id,
	cue,
	fecha_alta,
	nombre,
	anio_creacion,
	norma_creacion,
	norma_creacion_otra,
	norma_creacion_numero,
	telefono,
	interno,
	fax,
	email,
	sitio_web,
	observaciones,
	estado_id,
	ambito_id,

	last_user_id,
	created_at,
	updated_at,
	"version",
	deleted
) VALUES (
	NEW.id,
	NEW.establecimiento_id,
	NEW.cue,
	NEW.fecha_alta,
	NEW.nombre,
	NEW.anio_creacion,
	NEW.norma_creacion,
	NEW.norma_creacion_otra,
	NEW.norma_creacion_numero,
	NEW.telefono,
	NEW.interno,
	NEW.fax,
	NEW.email,
	NEW.sitio_web,
	NEW.observaciones,
	NEW.estado_id,
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

DROP TRIGGER IF EXISTS auditar ON registro_anexo;

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON registro_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo();

-- Delete


CREATE OR REPLACE FUNCTION auditar_registro_anexo_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_anexo_version
WHERE id = OLD.id;

INSERT INTO registro_anexo_version(
	id,
	establecimiento_id,
	cue,
	fecha_alta,
	nombre,
	anio_creacion,
	norma_creacion,
	norma_creacion_otra,
	norma_creacion_numero,
	telefono,
	interno,
	fax,
	email,
	sitio_web,
	observaciones,
	estado_id,
	ambito_id,

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
	OLD.anio_creacion,
	OLD.norma_creacion,
	OLD.norma_creacion_otra,
	OLD.norma_creacion_numero,
	OLD.telefono,
	OLD.interno,
	OLD.fax,
	OLD.email,
	OLD.sitio_web,
	OLD.observaciones,
	OLD.estado_id,
	OLD.ambito_id,

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
AFTER DELETE
ON registro_anexo
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_anexo_del();

--
--
--
-- Nuevo audit de extensión áulica

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
	id,
	establecimiento_id,
	nombre,
	observaciones,
	tipo_normativa_id,
	fecha_alta,
	normativa,
	anio_creacion,
	sitio_web,
	telefono,
	email,
	norma_creacion,
	norma_creacion_otra,
	norma_creacion_numero,
	estado_id,

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
	NEW.norma_creacion,
	NEW.norma_creacion_otra,
	NEW.norma_creacion_numero,
	NEW.estado_id,

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

--
-- Delete
--
CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_version(
	id,
	establecimiento_id,
	nombre,
	observaciones,
	tipo_normativa_id,
	fecha_alta,
	normativa,
	anio_creacion,
	sitio_web,
	telefono,
	email,
	norma_creacion,
	norma_creacion_otra,
	norma_creacion_numero,
	estado_id,

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
	OLD.norma_creacion,
	OLD.norma_creacion_otra,
	OLD.norma_creacion_numero,
	OLD.estado_id,

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
AFTER DELETE
ON registro_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_del();

--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('039', 'Registro', 'Ticket #167');

COMMIT;

