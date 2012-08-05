BEGIN;

DELETE FROM titulos_tipo_titulo ;

INSERT INTO titulos_tipo_titulo (nombre) VALUES ('Histórico'), ('Nuevo');

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('087', 'Títulos', 'Ticket #276');

COMMIT;
