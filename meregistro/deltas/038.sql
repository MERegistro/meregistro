-- Ticket #165

BEGIN;

-- Columnas

ALTER TABLE registro_anexo ADD COLUMN fax VARCHAR(100);
ALTER TABLE registro_anexo_version ADD COLUMN fax VARCHAR(100);

ALTER TABLE registro_anexo ADD COLUMN interno VARCHAR(10);
ALTER TABLE registro_anexo_version ADD COLUMN interno VARCHAR(10);

-- Credenciales
INSERT INTO seguridad_credencial (nombre, descripcion, grupo, aplicacion_id)
VALUES ('reg_editar_anexo_pendiente', 'Edición los datos de un anexo en estado Pendiente', 'Anexos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Registro'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_editar_anexo_pendiente')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
);
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_aprobar_registro')
);
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
	old_id,

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
	old_id,

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
	OLD.old_id,

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

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('038', 'Registro', 'Ticket #165');

COMMIT;

