BEGIN;

-------------------------------------

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reportes_seguimiento_cohortes')
);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('154', 'Reportes', 'Reporte de cohortes para RN');

COMMIT;
