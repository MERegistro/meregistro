BEGIN;

CREATE TABLE "registro_establecimiento_verificacion_datos" (
    "id" serial NOT NULL PRIMARY KEY,
    "establecimiento_id" integer NOT NULL UNIQUE REFERENCES "registro_establecimiento" ("id") DEFERRABLE INITIALLY DEFERRED,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "niveles" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilios" boolean NOT NULL,
    "autoridades" boolean NOT NULL,
    "info_edilicia" boolean NOT NULL,
    "conectividad" boolean NOT NULL,
    "completo" boolean NOT NULL
)
;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_establecimiento_verificar_datos', 'Verificar datos de Sedes', 2, 'Sedes');


CREATE TABLE "registro_extension_aulica_verificacion_datos" (
    "id" serial NOT NULL PRIMARY KEY,
    "extension_aulica_id" integer NOT NULL UNIQUE REFERENCES "registro_extension_aulica" ("id") DEFERRABLE INITIALLY DEFERRED,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "niveles" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilios" boolean NOT NULL,
    "info_edilicia" boolean NOT NULL,
    "conectividad" boolean NOT NULL,
    "completo" boolean NOT NULL
)
;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_extension_aulica_verificar_datos', 'Verificar datos de Extensiones Áulicas', 2, 'Extensiones Áulicas');

CREATE TABLE "registro_anexo_verificacion_datos" (
    "id" serial NOT NULL PRIMARY KEY,
    "anexo_id" integer NOT NULL UNIQUE REFERENCES "registro_anexo" ("id") DEFERRABLE INITIALLY DEFERRED,
    "datos_basicos" boolean NOT NULL,
    "contacto" boolean NOT NULL,
    "niveles" boolean NOT NULL,
    "turnos" boolean NOT NULL,
    "funciones" boolean NOT NULL,
    "domicilios" boolean NOT NULL,
    "info_edilicia" boolean NOT NULL,
    "conectividad" boolean NOT NULL,
    "completo" boolean NOT NULL
)
;

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_anexo_verificar_datos', 'Verificar datos de Anexos', 2, 'Anexos');



INSERT INTO deltas_sql (numero, app, comentario) VALUES ('049', 'Registro', '#186');

COMMIT;
