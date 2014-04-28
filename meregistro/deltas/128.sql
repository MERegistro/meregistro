BEGIN;

--
INSERT INTO titulos_estado_cohorte_establecimiento (nombre) VALUES ('Rechazada');
INSERT INTO titulos_estado_cohorte_anexo (nombre) VALUES ('Rechazada');
INSERT INTO titulos_estado_cohorte_extension_aulica (nombre) VALUES ('Rechazada');


-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('128', 'Títulos', 'RI rechaza asignación de cohorte - #388');

COMMIT;
