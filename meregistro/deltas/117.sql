BEGIN;

-------------------------------------

-- Credenciales


UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_consulta' WHERE nombre = 'validez_nacional_consulta';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_editar' WHERE nombre = 'validez_nacional_editar_solicitud';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_eliminar' WHERE nombre = 'validez_nacional_eliminar_solicitud';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_consulta_institucional' WHERE nombre = 'validez_nacional_consulta_institucional';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_create' WHERE nombre = 'validez_nacional_solicitud';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_control' WHERE nombre = 'validez_nacional_control';
UPDATE seguridad_credencial SET nombre = 'validez_nacional_solicitud_numerar' WHERE nombre = 'validez_nacional_numerar';


INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_validez_index', 'Lista de Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_validez_editar', 'Editar Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_validez_index')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_validez_editar')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('117', 'Validez Nacional', 'Editar validez de títulos - #353');

COMMIT;
