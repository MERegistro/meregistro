BEGIN;

ALTER TABLE validez_nacional_solicitud ADD COLUMN normativa_jurisdiccional_migrada character varying(255);

ALTER TABLE validez_nacional_validez_nacional ADD COLUMN carrera character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN titulo_nacional character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN primera_cohorte character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN ultima_cohorte character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN dictamen_cofev character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN normativas_nacionales character varying(255);
ALTER TABLE validez_nacional_validez_nacional ADD COLUMN normativa_jurisdiccional character varying(255);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('114', 'Carreras', '#351');

COMMIT;
