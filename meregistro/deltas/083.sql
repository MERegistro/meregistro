BEGIN;

ALTER TABLE registro_anexo_conexion_internet
   ALTER COLUMN tipo_conexion_id DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet
   ALTER COLUMN proveedor DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet
   ALTER COLUMN costo DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet
   ALTER COLUMN cantidad DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet
   ALTER COLUMN tipo_conexion_id DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet
   ALTER COLUMN proveedor DROP NOT NULL;


ALTER TABLE registro_establecimiento_conexion_internet
   ALTER COLUMN costo DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet
   ALTER COLUMN cantidad DROP NOT NULL;

ALTER TABLE registro_extension_aulica_conexion_internet
   ALTER COLUMN tipo_conexion_id DROP NOT NULL;

ALTER TABLE registro_extension_aulica_conexion_internet
   ALTER COLUMN proveedor DROP NOT NULL;

ALTER TABLE registro_extension_aulica_conexion_internet
   ALTER COLUMN costo DROP NOT NULL;

ALTER TABLE registro_extension_aulica_conexion_internet
   ALTER COLUMN cantidad DROP NOT NULL;




ALTER TABLE registro_anexo_conexion_internet_version
   ALTER COLUMN tipo_conexion_id DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet_version
   ALTER COLUMN proveedor DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet_version
   ALTER COLUMN costo DROP NOT NULL;

ALTER TABLE registro_anexo_conexion_internet_version
   ALTER COLUMN cantidad DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet_version
   ALTER COLUMN tipo_conexion_id DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet_version
   ALTER COLUMN proveedor DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet_version
   ALTER COLUMN costo DROP NOT NULL;

ALTER TABLE registro_establecimiento_conexion_internet_version
   ALTER COLUMN cantidad DROP NOT NULL;



INSERT INTO deltas_sql (numero, app, comentario) VALUES ('083', 'Registro', '#253');


COMMIT;
