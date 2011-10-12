-- Se pasa la columna horas_reloj de modalidad_distancia a titulo_jurisdiccional

-- La agrego en la tabla
ALTER TABLE titulos_titulo_jurisdiccional
ADD COLUMN horas_reloj integer unsigned;

-- Copio los datos
UPDATE titulos_titulo_jurisdiccional
SET horas_reloj = (SELECT horas_reloj FROM titulos_titulo_jurisd_modalidad_distancia WHERE titulo_id = titulos_titulo_jurisdiccional.id);

-- Elimino la columna NO FUNCIONA EN SQLITE
ALTER TABLE titulos_titulo_jurisd_modalidad_distancia
DROP COLUMN horas_reloj;
/*
-- WORKAROUND http://grass.osgeo.org/wiki/Sqlite_Drop_Column
BEGIN TRANSACTION;
-- TITULOS_TITULO_JURISD_MODALIDAD_DISTANCIA
CREATE TABLE "titulos_titulo_jurisd_modalidad_distancia_new" (
    "id" integer NOT NULL PRIMARY KEY,
    "titulo_id" integer NOT NULL REFERENCES "titulos_titulo_jurisdiccional" ("id"),
    "duracion" integer unsigned NOT NULL,
    "cuatrimestres" integer unsigned,
    "nro_dictamen" varchar(50)
);
-- Copio los datos
INSERT INTO titulos_titulo_jurisd_modalidad_distancia_new (id, titulo_id, duracion, cuatrimestres, nro_dictamen)
SELECT id, titulo_id, duracion, cuatrimestres, nro_dictamen FROM titulos_titulo_jurisd_modalidad_distancia;
-- Elimino la tabla
DROP TABLE titulos_titulo_jurisd_modalidad_distancia;
-- Renombro la nueva
ALTER TABLE titulos_titulo_jurisd_modalidad_distancia_new RENAME TO titulos_titulo_jurisd_modalidad_distancia;
COMMIT;
*/
