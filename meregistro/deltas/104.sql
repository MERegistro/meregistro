BEGIN;

---------------------------------------

DELETE FROM seguridad_rol_credenciales WHERE credencial_id =
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_consulta');

DELETE FROM seguridad_credencial_credenciales_hijas WHERE from_credencial_id =
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_consulta')
OR to_credencial_id = (SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_consulta');


DELETE FROM seguridad_credencial
WHERE nombre = 'tit_titulo_consulta';

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('104', 'Seguridad', 'Ticket #319');

COMMIT;
