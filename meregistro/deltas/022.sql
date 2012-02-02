-- Solicitud de registro de sede - Ticket #139
BEGIN;
---------------------------------------
--
--
-- Credenciales

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja')
);
---------------------------------------

ALTER TABLE registro_establecimiento ALTER COLUMN tipo_normativa_id DROP NOT NULL;
ALTER TABLE registro_establecimiento_version ALTER COLUMN tipo_normativa_id DROP NOT NULL;

ALTER TABLE registro_establecimiento ADD COLUMN solicitud_filename character varying(100);
ALTER TABLE registro_establecimiento_version ADD COLUMN solicitud_filename character varying(100);


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
	email,
	sitio_web,
	ambito_id,
	estado_id,
	old_id,
	identificacion_provincial,
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
  email,
  sitio_web,
  ambito_id,
  estado_id,
  old_id,
  identificacion_provincial,
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

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON registro_establecimiento;

CREATE TRIGGER auditar_del
AFTER DELETE
ON registro_establecimiento
FOR EACH ROW
EXECUTE PROCEDURE auditar_registro_establecimiento_del();



-- La secuencia está estropeada
SELECT SETVAL('registro_establecimiento_id_seq', (SELECT MAX(id) FROM registro_establecimiento));

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('022', 'Registro', 'Solicitud de registro de sede - Ticket #139');

--
COMMIT;
