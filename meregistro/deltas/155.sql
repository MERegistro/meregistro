BEGIN;

-------------------------------------

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('reportes_datos_basicos_unidades_servicio', 'Reporte de datos básicos de unidades de servicio', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'), 'Reportes');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_unidades_servicio')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_unidades_servicio')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_unidades_servicio')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_unidades_servicio')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('155', 'Reportes', 'Reporte unificado de unidades de servicio');

COMMIT;
