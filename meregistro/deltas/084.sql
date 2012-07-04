BEGIN;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_menu_ayuda', 'Acceso al Menú de Ayuda', 1, 'Seguridad y Usuarios');


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('084', 'Seguridad', '#260');


COMMIT;
