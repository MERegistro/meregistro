BEGIN;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id)
VALUES
  ('reg_anexo_completar', 'Completar datos de anexo', 2)
;

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
),
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Anexo'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
)
;

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('012', 'Seguridad', 'Credenciales #116');

COMMIT;
