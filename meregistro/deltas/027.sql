BEGIN;

INSERT INTO seguridad_rol_credenciales  (rol_id, credencial_id) VALUES (
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_modificar')
);

DELETE FROM seguridad_credencial WHERE nombre = 'revisar_jurisdiccion';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('027', 'Seguridad', 'Ticket #148');

COMMIT;
