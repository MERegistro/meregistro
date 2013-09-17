BEGIN;

-------------------------------------

-- Credenciales

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'tit_cohorte_seguimiento_consulta')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('120', 'Títulos', 'Seguimiento de Cohorte');

COMMIT;
