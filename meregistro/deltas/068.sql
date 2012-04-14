BEGIN;

UPDATE registro_tipo_compartido
SET descripcion = 'Otro Instituto Superior de Formación Docente'
WHERE descripcion ILIKE 'Otro Establecimiento de formación docente';

UPDATE registro_tipo_compartido
SET descripcion = 'Otro Tipo de Institución'
WHERE descripcion ILIKE 'Otro tipo de Establecimiento';

UPDATE registro_tipo_compartido
SET descripcion = 'Otra Institución Educativa'
WHERE descripcion ILIKE 'Establecimiento de Otro Nivel';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('068', 'Registro', '#218');

COMMIT;
