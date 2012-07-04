BEGIN;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('tit_menu_acceso', 'Acceso al Menú de Título', 3, 'Títulos');


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('082', 'Titulos', '#251');


COMMIT;
