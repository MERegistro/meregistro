BEGIN;

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud_consulta')
);
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'UsuarioConsultaInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_solicitud_consulta')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('139', 'Validez Nacional', 'RI puede consultar su solicitud de validez - #427');

COMMIT;
