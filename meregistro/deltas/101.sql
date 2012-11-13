BEGIN;

---------------------------------------

DELETE FROM titulos_estado_cohorte_establecimiento 
WHERE nombre = 'Aceptada por establecimiento';

DELETE FROM titulos_estado_cohorte_anexo 
WHERE nombre = 'Aceptada por anexo';

DELETE FROM titulos_estado_cohorte_extension_aulica 
WHERE nombre = 'Aceptada por extensión áulica';

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('101', 'Títulos', 'Avances de confirmación de cohorte - Ticket #300');

COMMIT;
