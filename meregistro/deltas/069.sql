BEGIN;

-- Modifica todos los ámbitos que quedaron después de la corrección del delta 066
/*
-- Versiones posteriores
UPDATE seguridad_ambito
SET path = CONCAT('/1/6/34/' || SUBSTRING(path FROM 9))
WHERE path LIKE '/1/5/34/%';

UPDATE seguridad_ambito
SET path = CONCAT('/1/7/35/' || SUBSTRING(path FROM 9))
WHERE path LIKE '/1/6/35/%';

UPDATE seguridad_ambito
SET path = CONCAT('/1/9/36/' || SUBSTRING(path FROM 9))
WHERE path LIKE '/1/7/36/%';
*/

UPDATE seguridad_ambito
SET path = '/1/6/34/' || SUBSTRING(path FROM 9)
WHERE path LIKE '/1/5/34/%';

UPDATE seguridad_ambito
SET path = '/1/7/35/' || SUBSTRING(path FROM 9)
WHERE path LIKE '/1/6/35/%';

UPDATE seguridad_ambito
SET path = '/1/9/36/' || SUBSTRING(path FROM 9)
WHERE path LIKE '/1/7/36/%';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('069', 'Seguridad', 'Ámbitos erróneos - #218');

COMMIT;
