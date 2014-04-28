BEGIN;

--

INSERT INTO seguridad_rol (nombre, descripcion, padre_id) VALUES
('SoloConsultaNacional', 'Sólo Consulta Ámbito Nacional', (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional')),
('SoloConsultaJurisdiccional', 'Sólo Consulta Ámbito Jurisdiccional', (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'));


-- Credenciales
--
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('reportes_datos_basicos_sedes', 'Reporte de datos básicos de sedes', 5, 'Reportes');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('reportes_datos_basicos_anexos', 'Reporte de datos básicos de anexos', 5, 'Reportes');
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('reportes_datos_basicos_extensiones_aulicas', 'Reporte de datos básicos de extensiones áulicas', 5, 'Reportes');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_sedes')),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_anexos')),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_extensiones_aulicas'))
;
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_sedes')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_anexos')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_extensiones_aulicas'))
;
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_sedes')),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_anexos')),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_extensiones_aulicas'))
;
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_sedes')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_anexos')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_datos_basicos_extensiones_aulicas'))
;

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('130', 'Reportes', 'Reportes de datos de Unidades Educativas - #404');

COMMIT;
