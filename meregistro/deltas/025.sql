BEGIN;

DELETE FROM seguridad_credencial WHERE nombre = 'revisar_jurisdiccion';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('025', 'Seguridad', 'Arreglo de credenciales');

COMMIT;
