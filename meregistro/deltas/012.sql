-- Cambio en el CUE de establecimiento - Ticket #111
BEGIN;

ALTER TABLE registro_establecimiento ALTER COLUMN cue TYPE VARCHAR(9);
-- Index: registro_establecimiento_cue_idx
-- DROP INDEX registro_establecimiento_cue_idx;
CREATE INDEX registro_establecimiento_cue_idx
  ON registro_establecimiento
  USING btree
  (cue);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('012', 'Registro', 'Cambio en el CUE de establecimiento - Ticket #111');

COMMIT;
