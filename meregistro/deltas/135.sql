BEGIN;

-------------------------------------

-- Credenciales

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('registro_modificar_cue', 'Modificar CUE de una Unidad Educativa', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Registro'), 'Registro');

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'registro_modificar_cue')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('135', 'Registro', 'Sólo RN puede cambiar CUE - #425');

COMMIT;
