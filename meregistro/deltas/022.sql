-- Solicitud de registro de sede - Ticket #139
BEGIN;
---------------------------------------
--
--
-- Credenciales

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja')
);
---------------------------------------

ALTER TABLE registro_establecimiento ALTER COLUMN tipo_normativa_id DROP NOT NULL;
ALTER TABLE registro_establecimiento_version ALTER COLUMN tipo_normativa_id DROP NOT NULL;

ALTER TABLE registro_establecimiento ADD COLUMN solicitud_filename character varying(100);
ALTER TABLE registro_establecimiento_version ADD COLUMN solicitud_filename character varying(100);

-- La secuencia está estropeada
SELECT SETVAL('registro_establecimiento_id_seq', (SELECT MAX(id) FROM registro_establecimiento));

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('022', 'Registro', 'Solicitud de registro de sede - Ticket #139');

--
COMMIT;
