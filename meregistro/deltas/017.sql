-- Cambios en credenciales de dependencia funcional - Ticket #109
BEGIN;
--

INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES ('Reportes', 'Reportes', '/reportes/');

-- Establecimientos
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reportes_listado_establecimientos', 'Listado de establecimientos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_establecimientos')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminTitulos'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_establecimientos')
);
-- Anexos
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reportes_listado_anexos', 'Listado de anexos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_anexos')
);
-- Extensiones áulicas
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reportes_listado_extensiones_aulicas', 'Listado de extensiones áulicas', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_extensiones_aulicas')
);
-- Dependencias funcionales
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reportes_listado_dependencias_funcionales', 'Listado de extensiones áulicas', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_dependencias_funcionales')
);
-- Usuarios
INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id) VALUES ('reportes_listado_usuarios', 'Listado de usuarios', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Reportes'));

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_usuarios')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_usuarios')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_listado_usuarios')
);

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('017', 'Reportes', 'Nueva aplicación de reportes');

--
COMMIT;
