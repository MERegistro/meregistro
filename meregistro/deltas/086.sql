BEGIN;

ALTER TABLE seguridad_usuario ADD COLUMN logins_count integer DEFAULT 0;
ALTER TABLE seguridad_usuario_version ADD COLUMN logins_count integer DEFAULT 0;

CREATE OR REPLACE FUNCTION auditar_seguridad_usuario()
  RETURNS trigger AS
$BODY$
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

  id,
  tipo_documento_id,
  documento,
  apellido,
  nombre,
  email,
  password,
  last_login,
  is_active,
  logins_count,
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
NEW.logins_count,

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


CREATE OR REPLACE FUNCTION auditar_seguridad_usuario_del()
  RETURNS trigger AS
$BODY$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM seguridad_usuario_version
WHERE id = OLD.id;

INSERT INTO seguridad_usuario_version(

  id,
  tipo_documento_id,
  documento,
  apellido,
  nombre,
  email,
  password,
  last_login,
  is_active,
  logins_count,
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
OLD.logins_count,

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


INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('seg_ver_datos_acceso', 'Ver Datos de Acceso', 1, 'Seguridad y Usuarios');


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('086', 'Seguridad', 'Ticket #273');

COMMIT;
