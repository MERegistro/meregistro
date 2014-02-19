BEGIN;


ALTER TABLE validez_nacional_solicitud ADD nro_expediente character varying(200);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('125', 'Validez Nacional', 'Número de expediente en Solicitud - #389');

COMMIT;
