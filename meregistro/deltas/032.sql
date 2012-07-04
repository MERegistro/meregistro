BEGIN;

UPDATE seguridad_credencial SET grupo = 'Dependencias Funcionales' WHERE nombre LIKE 'reg_df_%';
UPDATE seguridad_credencial SET grupo = 'Sedes' WHERE nombre LIKE 'reg_establecimiento%';
UPDATE seguridad_credencial SET grupo = 'Anexos' WHERE nombre LIKE 'reg_anexo%';
UPDATE seguridad_credencial SET grupo = 'Extensiones Áulicas' WHERE nombre LIKE 'reg_extension%';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('032', 'Seguridad', 'Ticket #152');

COMMIT;

