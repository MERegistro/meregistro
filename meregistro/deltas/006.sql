-- Nuevos campos de establecimiento - Ticket #71
BEGIN;
--
ALTER TABLE registro_establecimiento ADD COLUMN identificacion_provincial VARCHAR(100) NOT NULL DEFAULT '';
ALTER TABLE registro_establecimiento ADD COLUMN posee_subsidio BOOLEAN;
ALTER TABLE registro_establecimiento ADD COLUMN fax VARCHAR(100);

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('006', 'Registro', 'Nuevos campos en establecimiento - Ticket #71');

--
COMMIT;
