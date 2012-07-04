-- Cambios en credenciales de dependencia funcional - Ticket #109
BEGIN;
--
UPDATE seguridad_credencial 
SET nombre = 'reg_df_baja', descripcion = 'Baja de dependencia funcional'
WHERE id = (
	SELECT c.id FROM seguridad_credencial c
	LEFT JOIN seguridad_rol_credenciales rc ON rc.credencial_id = c.id
	WHERE nombre = 'reg_df_modificar'
	AND rc.id IS NULL
	LIMIT 1
);

INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'Referente'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_baja')
);

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('008', 'Registro', 'Cambios en credenciales de dependencia funcional - Ticket #109');

--
COMMIT;
