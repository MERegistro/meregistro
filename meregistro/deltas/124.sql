BEGIN;


INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('consulta_estadistica_nacional', 'Consulta de información estadística del sistema', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'), 'Estadística');
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'consulta_estadistica_nacional')
);
--

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('124', 'Registro', 'Consulta estadística referente nacional - #360');

COMMIT;
