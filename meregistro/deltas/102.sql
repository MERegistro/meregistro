BEGIN;
CREATE TABLE "consulta_validez_unidadeducativa" (
    "id" serial NOT NULL PRIMARY KEY,
    "cue" varchar(9) NOT NULL UNIQUE,
    "nombre" varchar(255) NOT NULL,
    "tipo_unidad_educativa" varchar(20) NOT NULL,
    "jurisdiccion_id" integer REFERENCES "registro_jurisdiccion" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "consulta_validez_titulo" (
    "id" serial NOT NULL PRIMARY KEY,
    "unidad_educativa_id" integer REFERENCES "consulta_validez_unidadeducativa" ("id") DEFERRABLE INITIALLY DEFERRED,
    "denominacion" varchar(255) NOT NULL,
    "primera" varchar(255) NOT NULL,
    "ultima" varchar(255) NOT NULL,
    "nroinfd" varchar(255) NOT NULL,
    "carrera" varchar(255) NOT NULL,
    "normativa_jurisdiccional" varchar(255) NOT NULL,
    "normativa_nacional" varchar(255) NOT NULL
)
;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('102', 'ConsultaValidez', 'Ticket #308');

COMMIT;
