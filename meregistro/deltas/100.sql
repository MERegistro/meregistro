BEGIN;

ALTER TABLE titulos_carrera_jurisdiccional_cohorte RENAME COLUMN primera_cohorte_autorizada TO anio_primera_cohorte;
ALTER TABLE titulos_carrera_jurisdiccional_cohorte RENAME COLUMN ultima_cohorte_autorizada TO anio_ultima_cohorte;
ALTER TABLE titulos_carrera_jurisdiccional_cohorte DROP COLUMN primera_cohorte_solicitada;
ALTER TABLE titulos_carrera_jurisdiccional_cohorte DROP COLUMN ultima_cohorte_solicitada;
ALTER TABLE titulos_carrera_jurisdiccional_cohorte ADD COLUMN cohortes_aprobadas INTEGER NOT NULL;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('100', 'Titulos', 'Reestructuración de código');

COMMIT;
