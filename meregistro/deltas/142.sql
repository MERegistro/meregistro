BEGIN;

--
DELETE FROM seguridad_rol_credenciales 
WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional')
AND credencial_id = (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_consulta');
--
DELETE FROM seguridad_rol_credenciales 
WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional')
AND credencial_id = (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_alta');
--
DELETE FROM seguridad_rol_credenciales 
WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional')
AND credencial_id = (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_modificar');
--
DELETE FROM seguridad_rol_credenciales 
WHERE rol_id = (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional')
AND credencial_id = (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_baja');

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('142', 'Seguridad', '#461');

COMMIT;
