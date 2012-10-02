BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('tit_carrera_asignar_titulos', 'Asignar Títulos Nacionales a Carreras', 3, 'Títulos');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_carrera_asignar_titulos')
);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('095', 'Titulos', 'Ticket #295');

COMMIT;
