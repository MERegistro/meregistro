-- Ticket #80
-- Describe REGISTRO_TIPO_EDUCACION
CREATE TABLE registro_tipo_educacion (
    id integer NOT NULL PRIMARY KEY,
    descripcion varchar(50) NOT NULL UNIQUE
);

INSERT INTO registro_tipo_educacion (id, descripcion) VALUES (1, 'Común');
INSERT INTO registro_tipo_educacion (id, descripcion) VALUES (2, 'Estatal');
INSERT INTO registro_tipo_educacion (id, descripcion) VALUES (3, 'Adultos');
INSERT INTO registro_tipo_educacion (id, descripcion) VALUES (4, 'Artística');
INSERT INTO registro_tipo_educacion (id, descripcion) VALUES (5, 'Otros');

-- WORKAROUND http://grass.osgeo.org/wiki/Sqlite_Drop_Column
BEGIN TRANSACTION;
-- 
CREATE TABLE registro_dependencia_funcional_new (
    id integer NOT NULL PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    jurisdiccion_id integer NOT NULL REFERENCES registro_jurisdiccion (id),
    gestion_jurisdiccion_id integer NOT NULL REFERENCES registro_gestion_jurisdiccion (id),
    tipo_gestion_id integer NOT NULL REFERENCES registro_tipo_gestion (id),
    tipo_dependencia_funcional_id integer NOT NULL REFERENCES registro_tipo_dependencia_funcional (id),
    tipo_educacion_id integer NOT NULL REFERENCES registro_tipo_educacion (id),
    ambito_id integer
);

-- Copio los datos
INSERT INTO registro_dependencia_funcional_new (id, nombre, jurisdiccion_id, gestion_jurisdiccion_id, tipo_gestion_id, tipo_dependencia_funcional_id, tipo_educacion_id, ambito_id)
SELECT id, nombre, jurisdiccion_id, gestion_jurisdiccion_id, tipo_gestion_id, tipo_dependencia_funcional_id, 2, ambito_id FROM registro_dependencia_funcional;

-- Elimino la tabla
DROP TABLE registro_dependencia_funcional;
-- Renombro la nueva
ALTER TABLE registro_dependencia_funcional_new RENAME TO registro_dependencia_funcional;
COMMIT;
