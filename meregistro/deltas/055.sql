BEGIN;

CREATE TABLE "registro_anexo_autoridades" (
    "id" serial NOT NULL PRIMARY KEY,
    "anexo_id" integer NOT NULL REFERENCES "registro_anexo" ("id") DEFERRABLE INITIALLY DEFERRED,
    "apellido" varchar(40) NOT NULL,
    "nombre" varchar(40) NOT NULL,
    "fecha_nacimiento" date,
    "cargo_id" integer REFERENCES "registro_autoridad_cargo" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_documento_id" integer REFERENCES "seguridad_tipo_documento" ("id") DEFERRABLE INITIALLY DEFERRED,
    "documento" varchar(20),
    "telefono" varchar(30),
    "celular" varchar(30),
    "email" varchar(255)
)
;

CREATE INDEX "registro_anexo_autoridades_anexo_id" ON "registro_anexo_autoridades" ("anexo_id");
CREATE INDEX "registro_anexo_autoridades_cargo_id" ON "registro_anexo_autoridades" ("cargo_id");
CREATE INDEX "registro_anexo_autoridades_tipo_documento_id" ON "registro_anexo_autoridades" ("tipo_documento_id");

ALTER TABLE registro_anexo_verificacion_datos ADD COLUMN "autoridades" boolean NOT NULL DEFAULT false;
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('055', 'Registro', 'Ticket #198');

COMMIT;
