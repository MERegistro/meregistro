-- Cambiar Estatal por Especial en tipos de educación
BEGIN;
--
UPDATE registro_tipo_educacion
SET descripcion = 'Especial'
WHERE descripcion = 'Estatal';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('002', 'Registro', 'Se cambió "Estatal" por "Especial" en "tipos de educación" - Ticket #80');
--
COMMIT;
