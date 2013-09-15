BEGIN;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES 
('tit_cohorte_seguimiento_consulta', 'Consultar Seguimiento de Cohorte', (SELECT id FROM seguridad_aplicacion WHERE nombre = 'Títulos'), 'Títulos');


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('119', 'Títulos', '#363');

COMMIT;
