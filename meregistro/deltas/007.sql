BEGIN;

DELETE FROM seguridad_rol_roles_asignables  WHERE from_rol_id IN (5,6,7, 9);

INSERT INTO seguridad_rol_roles_asignables  (from_rol_id, to_rol_id) VALUES 
(5, 5), (5, 6), (5, 7), (5, 9), 
(6, 6), (6, 7), (6, 9),
(7, 7), 
(9, 9);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('007', 'Seguridad', 'Roles asignables');

COMMIT;
