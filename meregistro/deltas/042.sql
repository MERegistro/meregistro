BEGIN;

CREATE TABLE "registro_extension_aulica_niveles" (
    "id" serial NOT NULL PRIMARY KEY,
    "extensionaulica_id" integer NOT NULL,
    "nivel_id" integer NOT NULL REFERENCES "registro_nivel" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("extensionaulica_id", "nivel_id")
)
;

ALTER TABLE "registro_extension_aulica_niveles" ADD CONSTRAINT "extensionaulica_id_refs_id_413a1592" FOREIGN KEY ("extensionaulica_id") REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE "registro_extension_aulica_funciones" (
    "id" serial NOT NULL PRIMARY KEY,
    "extensionaulica_id" integer NOT NULL,
    "funcion_id" integer NOT NULL REFERENCES "registro_funcion" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("extensionaulica_id", "funcion_id")
)
;

ALTER TABLE "registro_extension_aulica_funciones" ADD CONSTRAINT "extensionaulica_id_refs_id_1d60ea94" FOREIGN KEY ("extensionaulica_id") REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE "registro_extension_aulica_edificio_compartido_niveles" (
    "id" serial NOT NULL PRIMARY KEY,
    "extensionaulicainformacionedilicia_id" integer NOT NULL,
    "nivel_id" integer NOT NULL REFERENCES "registro_nivel" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("extensionaulicainformacionedilicia_id", "nivel_id")
)
;
CREATE TABLE "registro_extension_aulica_informacion_edilicia" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_dominio_id" integer REFERENCES "registro_tipo_dominio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_compartido_id" integer REFERENCES "registro_tipo_compartido" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "registro_extension_aulica_edificio_compartido_niveles" ADD CONSTRAINT "extensionaulicainformacionedilicia_id_refs_id_11a18f56" FOREIGN KEY ("extensionaulicainformacionedilicia_id") REFERENCES "registro_extension_aulica_informacion_edilicia" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "registro_extension_aulica_informacion_edilicia_extencion_aubb67" ON "registro_extension_aulica_informacion_edilicia" ("extension_aulica_id");
CREATE INDEX "registro_extension_aulica_informacion_edilicia_tipo_dominio_id" ON "registro_extension_aulica_informacion_edilicia" ("tipo_dominio_id");
CREATE INDEX "registro_extension_aulica_informacion_edilicia_tipo_compartda9c" ON "registro_extension_aulica_informacion_edilicia" ("tipo_compartido_id");

CREATE TABLE "registro_extension_aulica_conexion_internet" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_conexion_id" integer NOT NULL REFERENCES "registro_tipo_conexion" ("id") DEFERRABLE INITIALLY DEFERRED,
    "proveedor" varchar(30) NOT NULL,
    "tiene_conexion" boolean NOT NULL,
    "costo" numeric(12, 2) NOT NULL,
    "cantidad" integer NOT NULL
)
;
CREATE INDEX "registro_extension_aulica_conexion_internet_extension_aulica_id" ON "registro_extension_aulica_conexion_internet" ("extension_aulica_id");
CREATE INDEX "registro_extension_aulica_conexion_internet_tipo_conexion_id" ON "registro_extension_aulica_conexion_internet" ("tipo_conexion_id");


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('042', 'Registro', 'Ticket #148');

COMMIT;

