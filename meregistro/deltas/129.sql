BEGIN;

--

INSERT INTO seguridad_rol (nombre, descripcion, padre_id) VALUES
('SoloConsultaNacional', 'Sólo Consulta Ámbito Nacional', (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional')),
('SoloConsultaJurisdiccional', 'Sólo Consulta Ámbito Jurisdiccional', (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'));

-- Paths
UPDATE seguridad_rol
SET "path" = '/1/2/' || id || '/'
WHERE nombre IN('SoloConsultaNacional', 'SoloConsultaJurisdiccional')
;
-- Roles asignables
INSERT INTO seguridad_rol_roles_asignables (from_rol_id, to_rol_id)
VALUES (
  (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'),
  (SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional')
);
INSERT INTO seguridad_rol_roles_asignables (from_rol_id, to_rol_id)
VALUES (
  (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'),
  (SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional')
);
-- Tipos de ámbito asignables
INSERT INTO seguridad_rol_tipos_ambito_asignable (rol_id, tipoambito_id)
VALUES ((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), 1);
INSERT INTO seguridad_rol_tipos_ambito_asignable (rol_id, tipoambito_id)
VALUES ((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), 2);
-- Credenciales
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaNacional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'tit_cohorte_consulta'))
;
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')),
((SELECT id FROM seguridad_rol WHERE nombre = 'SoloConsultaJurisdiccional'), (SELECT id FROM seguridad_credencial WHERE nombre = 'tit_cohorte_consulta'))
;
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('129', 'Seguridad', 'Roles de sólo consulta - #387');

COMMIT;
