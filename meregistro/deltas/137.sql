BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('reportes_matricula', 'Reporte de Matrícula', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'), 'Reportes');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_matricula')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('137', 'Reportes', 'Reporte de Matrícula - #418');

COMMIT;
