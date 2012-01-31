-- Solicitud de registro de anexo - Ticket #140
BEGIN;
---------------------------------------
--
--
-- Credenciales

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_alta')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_baja')
);
---------------------------------------

ALTER TABLE registro_anexo ALTER COLUMN cue TYPE VARCHAR(9);
ALTER TABLE registro_anexo_version ALTER COLUMN cue TYPE VARCHAR(9);

CREATE UNIQUE INDEX registro_anexo_cue_idx
  ON registro_anexo
  USING btree
  (cue);


ALTER TABLE registro_anexo ADD COLUMN anio_creacion INTEGER;
ALTER TABLE registro_anexo_version ADD COLUMN anio_creacion INTEGER;

ALTER TABLE registro_anexo ADD COLUMN norma_creacion VARCHAR(100) NOT NULL;
ALTER TABLE registro_anexo_version ADD COLUMN norma_creacion VARCHAR(100) NOT NULL;

ALTER TABLE registro_anexo ADD COLUMN norma_creacion_otra VARCHAR(100);
ALTER TABLE registro_anexo_version ADD COLUMN norma_creacion_otra VARCHAR(100);

ALTER TABLE registro_anexo ADD COLUMN norma_creacion_numero VARCHAR(30) NOT NULL;
ALTER TABLE registro_anexo_version ADD COLUMN norma_creacion_numero VARCHAR(30) NOT NULL;

ALTER TABLE registro_anexo ADD COLUMN observaciones VARCHAR(255);
ALTER TABLE registro_anexo_version ADD COLUMN observaciones VARCHAR(255);

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

RETURN NEW;
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
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('023', 'Registro', 'Solicitud de registro de anexo - Ticket #140');

--
COMMIT;
