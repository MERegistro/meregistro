-- Cambios en dependencia funcional - Ticket #108
BEGIN;
--
-- Cambios en la tabla
ALTER TABLE registro_dependencia_funcional DROP COLUMN gestion_jurisdiccion_id;
ALTER TABLE registro_dependencia_funcional DROP COLUMN tipo_educacion_id;
ALTER TABLE registro_dependencia_funcional ALTER COLUMN nombre TYPE VARCHAR(255);

-- Constraint: registro_dependencia_funciona_jurisdiccion_id_tipo_gestion__key
-- ALTER TABLE registro_dependencia_funcional DROP CONSTRAINT registro_dependencia_funciona_jurisdiccion_id_tipo_gestion__key;
ALTER TABLE registro_dependencia_funcional
ADD CONSTRAINT registro_dependencia_funciona_jurisdiccion_id_tipo_gestion__key
UNIQUE(jurisdiccion_id, tipo_gestion_id, tipo_dependencia_funcional_id);

-- Elimino la tabla obsoleta
DROP TABLE registro_gestion_jurisdiccion;

-- No hago el truncate porque la tabla de dependencias funcionales puede tener datos
UPDATE registro_tipo_dependencia_funcional SET nombre = 'Dirección de Nivel Superior' WHERE id = 1;
UPDATE registro_tipo_dependencia_funcional SET nombre = 'Dirección de Educación Artística' WHERE id = 2;
UPDATE registro_tipo_dependencia_funcional SET nombre = 'Ministerio/Secretaría/Dirección de Cultura' WHERE id = 3;
UPDATE registro_tipo_dependencia_funcional SET nombre = 'Municipal' WHERE id = 4;
DELETE FROM registro_tipo_dependencia_funcional WHERE id = 5;

---------------------------------------
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('010', 'Registro', 'Cambios en dependencia funcional - Ticket #108');

--
COMMIT;
