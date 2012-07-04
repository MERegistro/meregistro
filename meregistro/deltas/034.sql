-- Ticket #161

BEGIN;

-- Editar establecimiento pendiente
INSERT INTO seguridad_credencial (nombre, descripcion, grupo, aplicacion_id)
VALUES ('reg_editar_establecimiento_pendiente', 'Edición los datos de un establecimiento en estado Pendiente', 'Sedes', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Registro'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_editar_establecimiento_pendiente')
);

-- Editar establecimiento
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
);

-- Modificación de columnas

ALTER TABLE registro_establecimiento ADD COLUMN interno VARCHAR(10);
ALTER TABLE registro_establecimiento_version ADD COLUMN interno VARCHAR(10);

ALTER TABLE registro_establecimiento DROP COLUMN identificacion_provincial;
ALTER TABLE registro_establecimiento_version DROP COLUMN identificacion_provincial;

-- Cambia el audit de datos


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
	old_id,
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
	NEW.old_id,
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
	old_id,
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
	OLD.old_id,
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
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('034', 'Registro', 'Ticket #162');

COMMIT;

