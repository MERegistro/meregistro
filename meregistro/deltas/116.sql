BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_numerar', 'Numerar Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_numerar')
);

-------------------------------------

ALTER TABLE validez_nacional_validez_nacional ADD COLUMN temporal BOOLEAN NOT NULL DEFAULT true;
UPDATE validez_nacional_validez_nacional SET temporal = false;

-- Actualizo algunas secuencias

SELECT setval('public.validez_nacional_validez_nacional_id_seq', 20000, true);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('116', 'Validez Nacional', 'Numeración de títulos - #352');

COMMIT;
