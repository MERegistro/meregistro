BEGIN;

-- 

UPDATE registro_region
SET nombre = '_CENTRO'
WHERE id = 3;

UPDATE registro_region
SET nombre = 'CUYO'
WHERE id = 4;

UPDATE registro_region
SET nombre = 'CENTRO'
WHERE id = 3;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('070', 'Registro', 'Cambio en regiones - Ticket #221');

COMMIT;
