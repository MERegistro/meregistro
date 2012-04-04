BEGIN;
--
--
UPDATE registro_anexo 
SET cue = LPAD(cue, 9, '0');
--
--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('062', 'Registro', 'CUEs de 1 dígito - Ticket #212');

COMMIT;
