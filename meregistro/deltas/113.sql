BEGIN;

-------------------------------------

ALTER TABLE titulos_carrera_jurisdiccional 
ADD CONSTRAINT carrera_jurisdiccional_carrera_jur_unique 
UNIQUE (carrera_id, jurisdiccion_id);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('113', 'Carreras', 'Cambios en carrera jurisdiccional - #344');

COMMIT;
