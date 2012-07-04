BEGIN;

DELETE FROM seguridad_perfil WHERE ambito_id > 25;
DELETE FROM seguridad_ambito WHERE id > 25;

insert into deltas_sql (numero, app, comentario) values ('003', 'Seguridad', 'Borrado de ambitos que no representan nada en el modelo.');

COMMIT;
