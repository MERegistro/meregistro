-- Solicitud de registro de extensión áulica - Ticket #141
BEGIN;

--!!! TRUNCATE registro_extension_aulica CASCADE;

---------------------------------------
--
--
-- Credenciales

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_alta')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_baja')
);
---------------------------------------

ALTER TABLE registro_extension_aulica ALTER COLUMN normativa DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN normativa DROP NOT NULL;

ALTER TABLE registro_extension_aulica ALTER COLUMN tipo_normativa_id DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN tipo_normativa_id DROP NOT NULL;

ALTER TABLE registro_extension_aulica ADD COLUMN cue VARCHAR(9);
ALTER TABLE registro_extension_aulica_version ADD COLUMN cue VARCHAR(9);

CREATE UNIQUE INDEX registro_ext_aulica_cue_idx
ON registro_extension_aulica
USING btree
(cue);


ALTER TABLE registro_extension_aulica ADD COLUMN norma_creacion VARCHAR(100) NOT NULL;
ALTER TABLE registro_extension_aulica_version ADD COLUMN norma_creacion VARCHAR(100) NOT NULL;

ALTER TABLE registro_extension_aulica ADD COLUMN norma_creacion_otra VARCHAR(100);
ALTER TABLE registro_extension_aulica_version ADD COLUMN norma_creacion_otra VARCHAR(100);

ALTER TABLE registro_extension_aulica ADD COLUMN norma_creacion_numero VARCHAR(30) NOT NULL;
ALTER TABLE registro_extension_aulica_version ADD COLUMN norma_creacion_numero VARCHAR(30) NOT NULL;

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
	old_id,

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

DROP TRIGGER IF EXISTS auditar_del ON registro_extension_aulica;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_extension_aulica
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_extension_aulica_del();
--
--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('024', 'Registro', 'Solicitud de registro de extensión áulica - Ticket #141');

--
COMMIT;
