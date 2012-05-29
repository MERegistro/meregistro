BEGIN;

CREATE TABLE "registro_tipo_subsidio" (
    "id" serial NOT NULL PRIMARY KEY,
    "descripcion" varchar(50) NOT NULL UNIQUE
)
;

INSERT INTO registro_tipo_subsidio (descripcion) VALUES
('0%'),
('Hasta el 25%'),
('Más del 25% y hasta el 50%'),
('Más del 50% y hasta el 75%'),
('Más del 75% y menos del 100%'),
('100%');

ALTER TABLE registro_establecimiento DROP COLUMN posee_subsidio;

ALTER TABLE registro_establecimiento 
ADD COLUMN "subsidio_id" integer REFERENCES "registro_tipo_subsidio" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE registro_anexo
ADD COLUMN "subsidio_id" integer REFERENCES "registro_tipo_subsidio" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE registro_extension_aulica
ADD COLUMN "subsidio_id" integer REFERENCES "registro_tipo_subsidio" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "registro_establecimiento_subsidio_id" ON "registro_establecimiento" ("subsidio_id");
CREATE INDEX "registro_anexo_subsidio_id" ON "registro_anexo" ("subsidio_id");
CREATE INDEX "registro_extension_aulica_subsidio_id" ON "registro_extension_aulica" ("subsidio_id");

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('077', 'Registro', 'Ticket #234');

COMMIT;
