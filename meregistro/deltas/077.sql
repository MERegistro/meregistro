BEGIN;

-- Actualizo algunas secuencias

SELECT setval('public.registro_tipo_conexion_id_seq', (SELECT MAX(id)+1 FROM registro_tipo_conexion), true);

SELECT setval('public.registro_estado_extension_aulica_id_seq', (SELECT MAX(id)+1 FROM registro_estado_extension_aulica), true);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('077', 'Registro', 'Ticket #236');

COMMIT;
