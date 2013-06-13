BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_consulta_institucional', 'Consulta Institucional de Solicitud Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_consulta_institucional')
);

-------------------------------------


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('111', 'Validez Nacional', 'Consulta de Validez Nacional Institucional - #332');

COMMIT;
