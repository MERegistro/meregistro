BEGIN;


-- Dependencia Temporal de Gestión Estatal de Ciudad Autónoma de Buenos Aires
-- El ambito parent era Chubut -> /1/5/34/
UPDATE seguridad_ambito
SET "path" = '/1/6/34/', parent_id = 6 
WHERE id = 34;

 
-- Dependencia Temporal de Gestión Estatal de Corrientes
-- El ambito parent era Ciudad Autónoma de Buenos Aires -> /1/6/35/
UPDATE seguridad_ambito
SET "path" = '/1/7/35/', parent_id = 7
WHERE id = 35;

 
-- Dependencia Temporal de Gestión Estatal de Entre Ríos
-- El ambito parent era Corrientes -> /1/7/36/
UPDATE seguridad_ambito
SET "path" = '/1/9/36/', parent_id = 9
WHERE id = 36;


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('066', 'Seguridad', 'Corrección de ámbitos de Dependencias funcionales - #216');

COMMIT;
