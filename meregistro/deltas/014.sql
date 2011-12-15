BEGIN;


DELETE FROM seguridad_rol_credenciales 
WHERE
rol_id IN (SELECT id FROM seguridad_rol WHERE nombre = 'AdminSistema') 
AND credencial_id IN (SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
;

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('014', 'Seguridad', 'Arreglo de credenciales del rol administrador del sistema');

COMMIT;
