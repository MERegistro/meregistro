BEGIN;

DELETE FROM seguridad_perfil WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre LIKE 'ReferenteRevisor');
DELETE FROM seguridad_rol_credenciales WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre LIKE 'ReferenteRevisor');
DELETE FROM seguridad_rol WHERE nombre LIKE 'ReferenteRevisor';

ALTER TABLE registro_establecimiento DROP COLUMN revisado_jurisdiccion;
ALTER TABLE registro_anexo DROP COLUMN revisado_jurisdiccion;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('011', 'Seguridad', 'Eliminar Revisor - Ticket #104');


COMMIT;
