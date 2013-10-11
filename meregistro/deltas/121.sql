BEGIN;

ALTER TABLE titulos_carrera ADD COLUMN "carrera_sin_orientacion" boolean NOT NULL DEFAULT '1';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('121', 'Títulos', 'Carrera nacional');

COMMIT;

