BEGIN;

ALTER TABLE seguridad_credencial ADD COLUMN "grupo" varchar(255);

UPDATE seguridad_credencial SET grupo = 'Unidades Educativas' WHERE nombre LIKE 'reg_%';
UPDATE seguridad_credencial SET grupo = 'Seguridad y Usuarios' WHERE nombre LIKE 'seg_%';
UPDATE seguridad_credencial SET grupo = 'Títulos' WHERE nombre LIKE 'tit_%';
UPDATE seguridad_credencial SET grupo = 'Otras' WHERE grupo IS NULL;

ALTER TABLE seguridad_credencial ALTER COLUMN grupo SET NOT NULL;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('028', 'Seguridad', 'Ticket #152');

COMMIT;

