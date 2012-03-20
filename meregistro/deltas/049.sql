BEGIN;

ALTER TABLE registro_tipo_conexion ALTER COLUMN nombre TYPE VARCHAR(100);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('049', '', 'Se cambia el campo nombre de tipo_conexion');

COMMIT;
