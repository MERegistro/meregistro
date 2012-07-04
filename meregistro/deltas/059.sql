BEGIN;

ALTER TABLE registro_nivel ALTER COLUMN nombre TYPE VARCHAR(100);

UPDATE registro_nivel
SET nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Inicial'
WHERE nombre = 'Inicial';

UPDATE registro_nivel
SET nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Primaria'
WHERE nombre = 'Primaria';

UPDATE registro_nivel
SET nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Secundaria'
WHERE nombre = 'Secundaria';

UPDATE registro_nivel
SET nombre = 'Oferta Carreras que Habilitan para Ejercer en la Educación Superior'
WHERE nombre = 'Superior';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('059', 'Registro', '#207');

COMMIT;
