BEGIN;


ALTER TABLE "registro_establecimiento_verificacion_datos" DROP COLUMN completo;

ALTER TABLE "registro_extension_aulica_verificacion_datos" DROP COLUMN completo;

ALTER TABLE "registro_anexo_verificacion_datos" DROP COLUMN completo;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('053', 'Registro', '#196');


COMMIT;
