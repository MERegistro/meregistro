-- Ticket #169

BEGIN;

-- Columnas

ALTER TABLE registro_anexo DROP COLUMN norma_creacion_numero;
ALTER TABLE registro_anexo_version DROP COLUMN norma_creacion_numero;

ALTER TABLE registro_anexo RENAME COLUMN norma_creacion_otra TO tipo_norma_otra;
ALTER TABLE registro_anexo_version RENAME COLUMN norma_creacion_otra TO tipo_norma_otra;

ALTER TABLE registro_anexo ADD COLUMN tipo_norma INTEGER;
ALTER TABLE registro_anexo_version ADD COLUMN tipo_norma INTEGER;

ALTER TABLE registro_anexo ADD CONSTRAINT registro_anexo_tipo_norma_id_fkey
	FOREIGN KEY (tipo_norma_id)
	REFERENCES registro_tipo_norma (id) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
      
ALTER TABLE registro_anexo ADD COLUMN tipo_normativa_id INTEGER;
ALTER TABLE registro_anexo_version ADD COLUMN tipo_normativa_id INTEGER;

ALTER TABLE registro_anexo ADD CONSTRAINT registro_anexo_tipo_normativa_id_fkey
	FOREIGN KEY (tipo_normativa_id)
	REFERENCES registro_tipo_normativa (id) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
      
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
	tipo_norma_otra,
	tipo_norma_id,
	tipo_normativa_id,
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
	NEW.tipo_norma_otra,
	NEW.tipo_norma_id,
	NEW.tipo_normativa_id,
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
	tipo_norma_otra,
	tipo_norma_id,
	tipo_normativa_id,
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
	OLD.tipo_norma_otra,
	OLD.tipo_normativa_id,
	OLD.tipo_norma_id,
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
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('041', 'Registro', 'Ticket #169');

COMMIT;

