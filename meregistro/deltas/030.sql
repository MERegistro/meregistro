BEGIN;


CREATE TABLE "registro_tipo_norma" (
    "id" serial NOT NULL PRIMARY KEY,
    "descripcion" varchar(50) NOT NULL UNIQUE
)
;

INSERT INTO registro_tipo_norma (descripcion) VALUES
('Decreto'), ('Resolución'), ('Disposición'), ('Dictamen'), ('Otra')
;

ALTER TABLE registro_establecimiento ADD COLUMN
"tipo_norma_id" integer REFERENCES "registro_tipo_norma" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE registro_establecimiento ADD COLUMN
"tipo_norma_otra" varchar(100);

CREATE INDEX "registro_establecimiento_tipo_norma_id" ON "registro_establecimiento" ("tipo_norma_id");

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('030', 'Registro', 'Ticket #150');

COMMIT;

