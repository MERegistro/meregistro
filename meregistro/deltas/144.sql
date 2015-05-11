BEGIN;


--- Se borra TODA la verificación de datos básicos de Sedes, Anexos y Extensiones

UPDATE registro_establecimiento_verificacion_datos SET datos_basicos = FALSE;

UPDATE registro_anexo_verificacion_datos SET datos_basicos = FALSE;

UPDATE registro_extension_aulica_verificacion_datos SET datos_basicos = FALSE;

---------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('144', 'Registro', '#467');

COMMIT;
