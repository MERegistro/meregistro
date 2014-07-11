BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_solicitud_informe', 'Informe de Solicitud de Validez', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud_informe')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('134', 'Validez Nacional', 'Informe de solicitud de RN - #390');

COMMIT;
