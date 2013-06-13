BEGIN;


UPDATE titulos_estado_cohorte_anexo SET nombre = 'Registrada' WHERE nombre = 'Aceptada';
UPDATE titulos_estado_cohorte_extension_aulica SET nombre = 'Registrada' WHERE nombre = 'Aceptada';
UPDATE titulos_estado_cohorte_establecimiento SET nombre = 'Registrada' WHERE nombre = 'Aceptada';

UPDATE titulos_estado_cohorte_anexo SET nombre = 'Aceptada' WHERE nombre = 'Asignada';
UPDATE titulos_estado_cohorte_extension_aulica SET nombre = 'Aceptada' WHERE nombre = 'Asignada';
UPDATE titulos_estado_cohorte_establecimiento SET nombre = 'Aceptada' WHERE nombre = 'Asignada';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('110', 'Titulos', 'Ticket #325');

COMMIT;
