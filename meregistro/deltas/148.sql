BEGIN;

--
INSERT INTO titulos_estado_cohorte_establecimiento (nombre) VALUES ('Finalizada');
INSERT INTO titulos_estado_cohorte_anexo (nombre) VALUES ('Finalizada');
INSERT INTO titulos_estado_cohorte_extension_aulica (nombre) VALUES ('Finalizada');


-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('148', 'Títulos', 'RI finaliza seguimiento de cohorte - #495');

COMMIT;
