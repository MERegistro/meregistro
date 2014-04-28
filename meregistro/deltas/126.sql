BEGIN;

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_alta')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_consulta')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_modificar')
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_normativa_nacional_baja')
);

-- Sacar vigencia de Normativas Nacionales
UPDATE titulos_normativa_nacional n
SET estado_id = (SELECT id FROM titulos_estado_normativa_nacional e where e.nombre = 'No vigente')
WHERE n.numero NOT IN('74/08', '83/09', '183/12', '000/00');

INSERT INTO titulos_normativa_nacional_estados (normativa_nacional_id, estado_id, fecha) 
SELECT n.id, n.estado_id, NOW() FROM titulos_normativa_nacional n WHERE n.numero NOT IN('74/08', '83/09', '183/12', '000/00');

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('126', 'Títulos', 'Estados y credenciales para poder administrar las normativas nacionales - #394');

COMMIT;
