BEGIN;

INSERT INTO validez_nacional_estado_solicitud (nombre) VALUES ('Retenido'), ('Evaluado');

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('138', 'Validez Nacional', 'Nuevos estados de Solicitud de Validez - #426');

COMMIT;
