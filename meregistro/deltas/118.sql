BEGIN;

ALTER TABLE validez_nacional_validez_nacional DROP COLUMN temporal;
ALTER TABLE validez_nacional_validez_nacional ALTER COLUMN normativa_jurisdiccional TYPE VARCHAR(999);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('118', 'Validez Nacional', 'Cambios en Validez - #352');

COMMIT;
