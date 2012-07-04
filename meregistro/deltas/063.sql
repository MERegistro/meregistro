BEGIN;

ALTER TABLE registro_tipo_norma ADD COLUMN "orden" integer;

UPDATE registro_tipo_norma SET orden = 1 WHERE descripcion = 'Decreto';
UPDATE registro_tipo_norma SET orden = 2 WHERE descripcion = 'Resolución';
UPDATE registro_tipo_norma SET orden = 3 WHERE descripcion = 'Disposición';
UPDATE registro_tipo_norma SET orden = 4 WHERE descripcion = 'Dictamen';
UPDATE registro_tipo_norma SET orden = 5 WHERE descripcion = 'Otra';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('063', 'Registro', 'Ticket #213 - Orden tipo norma');

COMMIT;

