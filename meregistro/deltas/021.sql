--- Cambio en el tipo de dato de last_login del usuario - Ticket #133
BEGIN;

ALTER TABLE seguridad_usuario DROP COLUMN last_login;
ALTER TABLE seguridad_usuario ADD COLUMN last_login TIMESTAMP WITHOUT TIME ZONE;
ALTER TABLE seguridad_usuario_version DROP COLUMN last_login;
ALTER TABLE seguridad_usuario_version ADD COLUMN last_login TIMESTAMP WITHOUT TIME ZONE;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('021', 'Seguridad', 'Cambio en el tipo de dato de last_login del usuario - Ticket #133');

COMMIT;
