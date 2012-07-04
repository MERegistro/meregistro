BEGIN;

ALTER TABLE registro_extension_aulica_version ADD COLUMN ambito_id INTEGER;

--
-- Reflejar cambios en las tablas de auditoria
--

DROP TRIGGER auditar ON registro_extension_aulica;


CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica()
  RETURNS trigger AS
$BODY$
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
    cue,
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
    origen_norma_id,
    ambito_id,
    
    last_user_id,
    created_at,
    updated_at,
    "version",
    deleted
)
VALUES (
    NEW.id,
    NEW.cue,
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
    NEW.origen_norma_id,
    NEW.ambito_id,

    NEW.last_user_id,
    CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
    NOW(),
    vers,
    FALSE
);


RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE TRIGGER auditar
  BEFORE INSERT OR UPDATE
  ON registro_extension_aulica
  FOR EACH ROW
  EXECUTE PROCEDURE auditar_registro_extension_aulica();


DROP TRIGGER auditar_del ON registro_extension_aulica;

CREATE OR REPLACE FUNCTION auditar_registro_extension_aulica_del()
  RETURNS trigger AS
$BODY$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM registro_extension_aulica_version
WHERE id = OLD.id;

INSERT INTO registro_extension_aulica_version(
    id,
    cue,
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
    origen_norma_id,
    ambito_id,
    
    last_user_id,
    created_at,
    updated_at,
    "version",
    deleted
)
VALUES (
    OLD.id,
    OLD.cue,
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
    OLD.origen_norma_id,
    OLD.ambito_id,
    
    OLD.last_user_id,
    CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
    NOW(),
    vers,
    TRUE
);

RETURN OLD;
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE TRIGGER auditar_del
  AFTER DELETE
  ON registro_extension_aulica
  FOR EACH ROW
  EXECUTE PROCEDURE auditar_registro_extension_aulica_del();

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('056', 'Registro', '#203');

COMMIT;
