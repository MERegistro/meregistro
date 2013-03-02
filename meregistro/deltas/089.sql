BEGIN;

-- Aplicación de Backend
INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES
('Backend', 'Backend', '/backend/');

-- Actualización de secuencia porque no me permite crear carreras

SELECT SETVAL('titulos_carrera_id_seq', (SELECT MAX(id) FROM titulos_carrera));

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('carreras_menu_acceso', 'Acceso al Menú de Carreras', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Backend'), 'Títulos');


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('089', 'Backend', '#286');


COMMIT;
