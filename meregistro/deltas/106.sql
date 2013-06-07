BEGIN;

UPDATE titulos_estado_cohorte_anexo SET nombre = 'Aceptada' WHERE nombre = 'Registrada';
UPDATE titulos_estado_cohorte_extension_aulica SET nombre = 'Aceptada' WHERE nombre = 'Registrada';
UPDATE titulos_estado_cohorte_establecimiento SET nombre = 'Aceptada' WHERE nombre = 'Registrada';
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('106', 'Titulos', 'Ticket #325');

COMMIT;
