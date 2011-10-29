-- Se cambia el tipo de la columna prefijo en jurisdicción

-- Cambio la columna NO FUNCIONA EN SQLITE
ALTER TABLE registro_jurisdiccion ALTER COLUMN prefijo varchar(3);
/*
-- WORKAROUND http://grass.osgeo.org/wiki/Sqlite_Drop_Column
BEGIN TRANSACTION;
-- 
CREATE TABLE registro_jurisdiccion_new (
    "id" integer NOT NULL PRIMARY KEY,
    "prefijo" varchar(3),
    "region_id" integer NOT NULL REFERENCES "registro_region" ("id"),
    "nombre" varchar(50) NOT NULL,
    "ambito_id" integer
)
-- Copio los datos
INSERT INTO registro_jurisdiccion_new (id, prefijo, region_id, nombre, ambito_id)
SELECT id, prefijo, region_id, nombre, ambito_id FROM registro_jurisdiccion;
-- Elimino la tabla
DROP TABLE registro_jurisdiccion;
-- Renombro la nueva
ALTER TABLE registro_jurisdiccion_new RENAME TO registro_jurisdiccion;
COMMIT;
*/
