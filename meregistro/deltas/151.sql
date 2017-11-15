BEGIN;


ALTER TABLE validez_nacional_solicitud ADD nro_expediente_gedo character varying(200);
-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('151', 'Validez Nacional', 'Número de expediente de GEDO en Solicitud');

COMMIT;
