BEGIN;

ALTER TABLE "seguridad_rol" ADD COLUMN "path" varchar(255);
ALTER TABLE "seguridad_rol" ADD COLUMN "padre_id" integer;

ALTER TABLE "seguridad_rol" ADD CONSTRAINT "padre_id_refs_id_6ca56f33" FOREIGN KEY ("padre_id") REFERENCES "seguridad_rol" ("id") DEFERRABLE INITIALLY DEFERRED;

UPDATE seguridad_rol SET path = '/' || id || '/' WHERE nombre = 'AdminSeguridad';
UPDATE seguridad_rol SET path = (SELECT path FROM seguridad_rol WHERE nombre = 'AdminSeguridad') || id || '/' WHERE nombre = 'AdminNacional';
UPDATE seguridad_rol SET path = (SELECT path FROM seguridad_rol WHERE nombre = 'AdminNacional') || id || '/' WHERE nombre = 'ReferenteJurisdiccional';
UPDATE seguridad_rol SET path = (SELECT path FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional') || id || '/' WHERE nombre = 'ReferenteInstitucional';

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('067', 'Seguridad', '#166');

COMMIT;
