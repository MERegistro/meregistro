-- Agrega la credencial de ver detalle del establecimiento al rol administrador de títulos nacionales - Ticket #123

BEGIN;
--

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminTitulos'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver')
);
---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('018', 'Seguridad', 'Credencial de ver detalle del establecimiento al rol administrador de títulos nacionales - Ticket #123');

--
COMMIT;
