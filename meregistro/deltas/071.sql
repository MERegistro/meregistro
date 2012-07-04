BEGIN;

CREATE TABLE "seguridad_tipoambito" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "descripcion" varchar(100) NOT NULL
)
;

INSERT INTO seguridad_tipoambito (id, nombre, descripcion) VALUES
(1, 'Superior', 'Superior'),
(2, 'Jurisdiccion', 'Jurisdicción'),
(3, 'DependenciaFuncional', 'Dependencia Funcional'),
(4, 'Sede', 'Sede'),
(5, 'Anexo', 'Anexo'),
(6, 'ExtensionAulica', 'Extensión Áulica');

ALTER TABLE seguridad_ambito ADD COLUMN "tipo_id" integer REFERENCES "seguridad_tipoambito" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "seguridad_ambito_tipo_id" ON "seguridad_ambito" ("tipo_id");

UPDATE seguridad_ambito SET tipo_id = 2 WHERE id IN (SELECT ambito_id FROM registro_jurisdiccion);
UPDATE seguridad_ambito SET tipo_id = 3 WHERE id IN (SELECT ambito_id FROM registro_dependencia_funcional);
UPDATE seguridad_ambito SET tipo_id = 4 WHERE id IN (SELECT ambito_id FROM registro_establecimiento);
UPDATE seguridad_ambito SET tipo_id = 5 WHERE id IN (SELECT ambito_id FROM registro_anexo);
UPDATE seguridad_ambito SET tipo_id = 6 WHERE id IN (SELECT ambito_id FROM registro_extension_aulica);
UPDATE seguridad_ambito SET tipo_id = 1 WHERE tipo_id IS NULL;

CREATE TABLE "seguridad_rol_tipos_ambito_asignable" (
    "id" serial NOT NULL PRIMARY KEY,
    "rol_id" integer NOT NULL,
    "tipoambito_id" integer NOT NULL REFERENCES "seguridad_tipoambito" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("rol_id", "tipoambito_id")
)
;

ALTER TABLE "seguridad_rol_tipos_ambito_asignable" ADD CONSTRAINT "rol_id_refs_id_291a3da2" FOREIGN KEY ("rol_id") REFERENCES "seguridad_rol" ("id") DEFERRABLE INITIALLY DEFERRED;

INSERT INTO seguridad_rol_tipos_ambito_asignable (rol_id, tipoambito_id) VALUES
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 1),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 2),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 3),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 4),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 5),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad'), 6),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 1),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 2),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 3),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 4),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 5),
((SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional'), 6),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 2),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 3),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 4),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 5),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 6),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 4),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 5),
((SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional'), 6);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('071', 'Seguridad', 'Ticket #222');

COMMIT;
