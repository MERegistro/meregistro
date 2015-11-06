-- Cambios en credenciales de dependencia funcional - Ticket #109
BEGIN;
--

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES ('validez_nacional_solicitud_informe_impresion', 'Vista de impresión de Solicitud de Validez Nacional', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Reportes');

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud_informe_impresion')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud_informe_impresion')
);

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('147', 'Validez Nacional', 'Informe de impresión de Solicitud de Validez');

--
COMMIT;
