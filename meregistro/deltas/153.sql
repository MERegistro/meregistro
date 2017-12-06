BEGIN;

-------------------------------------

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_matricula')
);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('153', 'Registro', 'Reporte de matrícula para RN');

COMMIT;
