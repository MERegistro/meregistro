BEGIN;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('seg_backend', 'Backend', 1, 'Seguridad y Usuarios');

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_backend')
);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('080', 'Seguridad', '#248');


COMMIT;
