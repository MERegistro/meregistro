BEGIN;

DELETE FROM seguridad_perfil;
DELETE FROM seguridad_rol_credenciales;
DELETE FROM seguridad_rol_roles_asignables;
DELETE FROM seguridad_rol;

INSERT INTO seguridad_rol (id, nombre, descripcion) VALUES
(1, 'AdminSeguridad', 'Administrador de Seguridad'),
(2, 'AdminTitulos', 'Administrador de Títulos Nacionales'),
(3, 'Referente','Referente jurisdiccional'),
(4, 'ReferenteInstitucional', 'Referente Institucional');

INSERT INTO seguridad_rol_roles_asignables (id, from_rol_id, to_rol_id) VALUES
(1,1,1),
(2,1,2),
(3,1,3),
(4,1,4),
(5,2,2),
(6,2,3),
(7,2,4),
(8,4,3),
(9,4,4),
(10,3,3);

SELECT setval('public.seguridad_rol_roles_asignables_id_seq', 11, true);
SELECT setval('public.seguridad_rol_id_seq', 5, true);


SELECT pg_catalog.setval('seguridad_rol_credenciales_id_seq', 399, true);

INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (361, 2, 9);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (362, 2, 19);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (363, 2, 17);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (364, 2, 15);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (365, 1, 1);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (366, 1, 2);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (367, 1, 3);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (368, 1, 4);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (369, 1, 5);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (370, 1, 6);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (371, 4, 65);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (372, 4, 2);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (373, 4, 3);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (374, 4, 4);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (375, 4, 5);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (376, 4, 6);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (377, 4, 10);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (378, 4, 12);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (379, 4, 14);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (380, 4, 15);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (381, 4, 17);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (382, 4, 19);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (383, 4, 23);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (384, 3, 2);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (385, 3, 3);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (386, 3, 4);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (387, 3, 5);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (388, 3, 6);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (389, 3, 7);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (390, 3, 8);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (391, 3, 12);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (392, 3, 15);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (393, 3, 17);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (394, 3, 19);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (395, 3, 21);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (396, 3, 22);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (397, 3, 23);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (398, 3, 24);
INSERT INTO seguridad_rol_credenciales (id, rol_id, credencial_id) VALUES (399, 3, 25);


INSERT INTO seguridad_perfil (usuario_id, rol_id, ambito_id, fecha_asignacion) VALUES (1,1,1, NOW());

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('015', 'Seguridad', '#113');


COMMIT;
