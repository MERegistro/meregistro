BEGIN;

--
DELETE FROM titulos_titulos_nacionales_carreras
WHERE carrera_id = (SELECT c.id FROM titulos_carrera c WHERE c.nombre = 'Profesorado de Agronomía')
AND titulonacional_id = (SELECT t.id FROM titulos_titulo_nacional t WHERE t.nombre = 'Profesor/a de Educación Secundaria en Antropología');
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('131', 'Títulos', 'Título mal asignado a carrera - #410');

COMMIT;
