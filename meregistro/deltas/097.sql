BEGIN;

UPDATE seguridad_credencial 
SET grupo = 'Carreras Jurisdiccionales'
WHERE nombre LIKE 'tit_carrera_jurisdiccional%';

UPDATE seguridad_credencial 
SET grupo = 'Normativas Jurisdiccionales'
WHERE nombre LIKE 'tit_nor_jur%';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('097', 'Seguridad', 'Ticket #304');

COMMIT;
