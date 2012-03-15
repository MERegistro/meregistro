BEGIN;

ALTER TABLE registro_establecimiento_conexion_internet
   ALTER COLUMN proveedor DROP NOT NULL;


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('047', 'Registro', '#183');

COMMIT;
