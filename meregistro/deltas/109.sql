BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('validez_nacional_eliminar_solicitud', 'Eliminar Solicitud Validez Nacional de Títulos', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Validez Nacional'), 'Validez Nacional');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_eliminar_solicitud')
);
--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_eliminar_solicitud')
);

-------------------------------------


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('109', 'Validez Nacional', '#322');

COMMIT;
