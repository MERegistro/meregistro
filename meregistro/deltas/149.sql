BEGIN;

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
);

-------------------------------------



INSERT INTO deltas_sql (numero, app, comentario) VALUES ('149', 'Registro', 'Credencial de EXT AULICA a RI');

COMMIT;
