BEGIN;

ALTER TABLE registro_establecimiento
   ALTER COLUMN norma_creacion DROP NOT NULL;


ALTER TABLE registro_anexo
   ALTER COLUMN norma_creacion DROP NOT NULL;

ALTER TABLE registro_extension_aulica
   ALTER COLUMN norma_creacion DROP NOT NULL;

ALTER TABLE registro_extension_aulica
   ALTER COLUMN norma_creacion_numero DROP NOT NULL;

ALTER TABLE registro_extension_aulica
   ALTER COLUMN observaciones DROP NOT NULL;

ALTER TABLE registro_establecimiento_domicilio
   ALTER COLUMN calle DROP NOT NULL;

ALTER TABLE registro_establecimiento_domicilio
   ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_establecimiento_domicilio
   ALTER COLUMN cp DROP NOT NULL;

ALTER TABLE registro_anexo_domicilio
   ALTER COLUMN calle DROP NOT NULL;

ALTER TABLE registro_anexo_domicilio
   ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_anexo_domicilio
   ALTER COLUMN cp DROP NOT NULL;

ALTER TABLE registro_extension_aulica_domicilio
   ALTER COLUMN calle DROP NOT NULL;

ALTER TABLE registro_extension_aulica_domicilio
   ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_extension_aulica_domicilio
   ALTER COLUMN cp DROP NOT NULL;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('045', 'Registro', '#177');

COMMIT;
