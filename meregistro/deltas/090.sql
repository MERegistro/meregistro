BEGIN;

DELETE FROM seguridad_rol_credenciales WHERE credencial_id IN
(
	SELECT id FROM seguridad_credencial WHERE nombre = 'carreras_menu_acceso'
);

DELETE FROM seguridad_credencial WHERE nombre IN
(
    'carreras_menu_acceso'
);

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('tit_carrera_consulta', 'Listar Carreras', 3, 'Carreras');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('tit_carrera_alta', 'Alta de Carreras', 3, 'Carreras');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('tit_carrera_modificar', 'Modificar Carreras', 3, 'Carreras');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('tit_carrera_baja', 'Baja de Carreras', 3, 'Carreras');


INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_consulta')
);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('090', 'Titulos', 'Ticket #290');

COMMIT;

