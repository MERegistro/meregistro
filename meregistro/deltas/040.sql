BEGIN;

DELETE FROM seguridad_rol_credenciales WHERE credencial_id IN
(
    SELECT id FROM seguridad_credencial WHERE nombre LIKE 'reporte_%'
);

DELETE FROM seguridad_credencial WHERE nombre LIKE 'reporte_%';



INSERT INTO deltas_sql (numero, app, comentario) VALUES ('040', 'Seguridad', 'Ticket #163 y #164');

COMMIT;

