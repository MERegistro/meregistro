BEGIN;

CREATE TABLE "seguridad_configuracion_solapas_extension_aulica" (
    "id" serial NOT NULL PRIMARY KEY,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "alcances" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilio" boolean NOT NULL,
    "informacion_edilicia" boolean NOT NULL,
    "conexion_internet" boolean NOT NULL,
    "matricula" boolean NOT NULL
)
;

INSERT INTO seguridad_configuracion_solapas_extension_aulica VALUES
(1, true, true, true, true, true, true, true, true, true);

CREATE TABLE "seguridad_configuracion_solapas_establecimiento" (
    "id" serial NOT NULL PRIMARY KEY,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "alcances" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilio" boolean NOT NULL,
    "autoridad" boolean NOT NULL,
    "informacion_edilicia" boolean NOT NULL,
    "conexion_internet" boolean NOT NULL,
    "matricula" boolean NOT NULL
)
;

INSERT INTO seguridad_configuracion_solapas_establecimiento VALUES
(1, true, true, true, true, true, true, true, true, true, true);

CREATE TABLE "seguridad_configuracion_solapas_anexo" (
    "id" serial NOT NULL PRIMARY KEY,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "alcances" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilio" boolean NOT NULL,
    "autoridad" boolean NOT NULL,
    "informacion_edilicia" boolean NOT NULL,
    "conexion_internet" boolean NOT NULL,
    "matricula" boolean NOT NULL
)
;


INSERT INTO seguridad_configuracion_solapas_anexo VALUES
(1, true, true, true, true, true, true, true, true, true, true);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('081', 'Seguridad', '#248');


COMMIT;
