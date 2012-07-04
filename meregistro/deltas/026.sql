BEGIN;

INSERT INTO seguridad_rol_credenciales  (rol_id, credencial_id) VALUES (
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('026', 'Seguridad', 'Ticket #148');

COMMIT;
