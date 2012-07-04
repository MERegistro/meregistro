-- Cambiar Unidad de extensión por Extensión áulica - Ticket #95
BEGIN;
--
DROP TABLE registro_unidad_extension_baja;
DROP TABLE registro_unidad_extension_domicilio;
DROP TABLE registro_unidad_extension_estados;
DROP TABLE registro_unidades_extension_turnos;

DROP TABLE titulos_cohorte_unidad_extension_estados;
DROP TABLE titulos_cohortes_unidades_extension;

DROP TABLE registro_unidad_extension;
DROP TABLE registro_estado_unidad_extension;
DROP TABLE titulos_estado_cohorte_unidad_extension;
--
--
CREATE TABLE "registro_estado_extension_aulica" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(50) NOT NULL UNIQUE
)
;
INSERT INTO registro_estado_extension_aulica (id, nombre) VALUES (1, 'Pendiente');
INSERT INTO registro_estado_extension_aulica (id, nombre) VALUES (2, 'Baja');
INSERT INTO registro_estado_extension_aulica (id, nombre) VALUES (3, 'Registrada');
INSERT INTO registro_estado_extension_aulica (id, nombre) VALUES (4, 'No vigente');
INSERT INTO registro_estado_extension_aulica (id, nombre) VALUES (5, 'Vigente');
--
CREATE TABLE "registro_extensiones_aulicas_turnos" (
    "id" serial NOT NULL PRIMARY KEY,
    "extensionaulica_id" integer NOT NULL,
    "turno_id" integer NOT NULL REFERENCES "registro_turno" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("extensionaulica_id", "turno_id")
)
;
CREATE TABLE "registro_extension_aulica" (
    "id" serial NOT NULL PRIMARY KEY,
    "establecimiento_id" integer NOT NULL REFERENCES "registro_establecimiento" ("id") DEFERRABLE INITIALLY DEFERRED,
    "nombre" varchar(255) NOT NULL,
    "observaciones" varchar(255) NOT NULL,
    "tipo_normativa_id" integer NOT NULL REFERENCES "registro_tipo_normativa" ("id") DEFERRABLE INITIALLY DEFERRED,
    "fecha_alta" date,
    "normativa" varchar(100) NOT NULL,
    "anio_creacion" integer,
    "sitio_web" varchar(255),
    "telefono" varchar(100),
    "email" varchar(255),
    "estado_id" integer NOT NULL REFERENCES "registro_estado_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "old_id" integer
)
;
ALTER TABLE "registro_extensiones_aulicas_turnos" ADD CONSTRAINT "extensionaulica_id_refs_id_a87a1994" FOREIGN KEY ("extensionaulica_id") REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED;
--
CREATE TABLE "registro_extension_aulica_domicilio" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_domicilio_id" integer NOT NULL REFERENCES "registro_tipo_domicilio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "localidad_id" integer NOT NULL REFERENCES "registro_localidad" ("id") DEFERRABLE INITIALLY DEFERRED,
    "calle" varchar(100) NOT NULL,
    "altura" varchar(5) NOT NULL,
    "referencia" varchar(255),
    "cp" varchar(20) NOT NULL
)
;
CREATE TABLE "registro_extension_aulica_estados" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "estado_id" integer NOT NULL REFERENCES "registro_estado_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "fecha" date NOT NULL
)
;
CREATE TABLE "registro_extension_aulica_baja" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "observaciones" varchar(255) NOT NULL,
    "fecha_baja" date NOT NULL
)
;
-----------------------
CREATE TABLE "titulos_estado_cohorte_extension_aulica" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(50) NOT NULL UNIQUE
)
;
INSERT INTO titulos_estado_cohorte_extension_aulica (id, nombre) VALUES (1, 'Asignada');
INSERT INTO titulos_estado_cohorte_extension_aulica (id, nombre) VALUES (2, 'Aceptada por extensión áulica');
INSERT INTO titulos_estado_cohorte_extension_aulica (id, nombre) VALUES (3, 'Registrada');
--
CREATE TABLE "titulos_cohortes_extensiones_aulicas" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL,
    "cohorte_id" integer NOT NULL REFERENCES "titulos_cohorte" ("id") DEFERRABLE INITIALLY DEFERRED,
    "oferta" boolean,
    "inscriptos" integer CHECK ("inscriptos" >= 0),
    "estado_id" integer NOT NULL REFERENCES "titulos_estado_cohorte_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("extension_aulica_id", "cohorte_id")
)
;
ALTER TABLE "titulos_cohortes_extensiones_aulicas" ADD CONSTRAINT "extension_aulica_id_refs_id_cc3e6bb6" FOREIGN KEY ("extension_aulica_id") REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED;
--
CREATE TABLE "titulos_cohorte_extension_aulica_estados" (
    "id" serial NOT NULL PRIMARY KEY,
    "cohorte_extension_aulica_id" integer NOT NULL REFERENCES "titulos_cohortes_extensiones_aulicas" ("id") DEFERRABLE INITIALLY DEFERRED,
    "estado_id" integer NOT NULL REFERENCES "titulos_estado_cohorte_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "fecha" date NOT NULL
)
;

--
--
-- Credenciales

UPDATE seguridad_credencial
SET nombre = 'reg_extension_aulica_alta', descripcion = 'Alta nueva extensión áulica'
WHERE nombre = 'reg_unidad_extension_alta';

UPDATE seguridad_credencial
SET nombre = 'reg_extension_aulica_modificar', descripcion = 'Modificar datos de extensión áulica'
WHERE nombre = 'reg_unidad_extension_modificar';

UPDATE seguridad_credencial
SET nombre = 'reg_extension_aulica_consulta', descripcion = 'Consultar datos de extensión áulica'
WHERE nombre = 'reg_unidad_extension_consulta';

UPDATE seguridad_credencial
SET nombre = 'reg_extension_aulica_baja', descripcion = 'Baja de extensión áulica'
WHERE nombre = 'reg_unidad_extension_baja';

---------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('005', 'Registro', 'Cambios de Unidad de Extensión por Extensión Áulica - Ticket #95');

--
COMMIT;
