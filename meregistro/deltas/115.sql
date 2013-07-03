BEGIN;


ALTER TABLE titulos_cohortes_establecimientos DROP COLUMN oferta;
ALTER TABLE titulos_cohortes_establecimientos DROP COLUMN emite;

ALTER TABLE titulos_cohortes_anexos DROP COLUMN oferta;
ALTER TABLE titulos_cohortes_anexos DROP COLUMN emite;

ALTER TABLE titulos_cohortes_extensiones_aulicas DROP COLUMN oferta;



INSERT INTO deltas_sql (numero, app, comentario) VALUES ('115', 'Títulos', '#345');

COMMIT;
