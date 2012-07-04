
BEGIN;
---------------------------------------

ALTER TABLE registro_establecimiento_domicilio ALTER COLUMN altura TYPE VARCHAR(15);
ALTER TABLE registro_establecimiento_domicilio_version ALTER COLUMN altura TYPE VARCHAR(15);

ALTER TABLE registro_anexo_domicilio ALTER COLUMN altura TYPE VARCHAR(15);
ALTER TABLE registro_anexo_domicilio_version ALTER COLUMN altura TYPE VARCHAR(15);

ALTER TABLE registro_extension_aulica_domicilio ALTER COLUMN altura TYPE VARCHAR(15);
ALTER TABLE registro_extension_aulica_domicilio_version ALTER COLUMN altura TYPE VARCHAR(15);

--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('043', 'Registro', 'Cambios para domicilios - Tickets #172/3/4');

--
COMMIT;
