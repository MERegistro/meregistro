-- Se elimina el tipo de título del título jurisdiccional

-- Elimino la columna NO FUNCIONA EN SQLITE
ALTER TABLE titulos_titulo_jurisdiccional DROP COLUMN tipo_titulo;
/*
-- WORKAROUND http://grass.osgeo.org/wiki/Sqlite_Drop_Column
BEGIN TRANSACTION;
-- 
CREATE TABLE "titulos_titulo_jurisdiccional_new" (
    "id" integer NOT NULL PRIMARY KEY,
    "titulo_id" integer NOT NULL REFERENCES "titulos_titulo" ("id"),
    "jurisdiccion_id" integer NOT NULL REFERENCES "registro_jurisdiccion" ("id"),
    "estado_id" integer NOT NULL REFERENCES "titulos_estado_titulo_jurisdiccional" ("id")
, "revisado_jurisdiccion", horas_reloj integer unsigned);
-- Copio los datos
INSERT INTO titulos_titulo_jurisd_modalidad_distancia_new (id, titulo_id, jurisdiccion_id, estado_id, revisado_jurisdiccion, horas_reloj)
SELECT id, titulo_id, jurisdiccion_id, estado_id, revisado_jurisdiccion, horas_reloj FROM titulos_titulo_jurisdiccional;
-- Elimino la tabla
DROP TABLE titulos_titulo_jurisdiccional;
-- Renombro la nueva
ALTER TABLE titulos_titulo_jurisdiccional_new RENAME TO titulos_titulo_jurisdiccional;
COMMIT;
*/
