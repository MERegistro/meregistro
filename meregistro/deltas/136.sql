BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('reportes_seguimiento_cohortes', 'Reporte de Seguimiento de Cohortes', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'), 'Reportes');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_seguimiento_cohortes')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('136', 'Reportes', 'Reporte de Seguimiento de Cohortes - #417');

COMMIT;
