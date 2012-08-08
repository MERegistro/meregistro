BEGIN;

ALTER TABLE seguridad_configuracion_solapas_extension_aulica 
RENAME COLUMN autoridades TO autoridad;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('088', 'Registro', 'Ticket #281');

COMMIT;
