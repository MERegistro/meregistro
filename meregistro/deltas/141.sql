BEGIN;

ALTER TABLE registro_establecimiento ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_establecimiento ADD COLUMN posee_representantes_estudiantiles boolean NULL;
ALTER TABLE registro_establecimiento_version ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_establecimiento_version ADD COLUMN posee_representantes_estudiantiles boolean NULL;

ALTER TABLE registro_anexo ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_anexo ADD COLUMN posee_representantes_estudiantiles boolean NULL;
ALTER TABLE registro_anexo_version ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_anexo_version ADD COLUMN posee_representantes_estudiantiles boolean NULL;

ALTER TABLE registro_extension_aulica ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_extension_aulica ADD COLUMN posee_representantes_estudiantiles boolean NULL;
ALTER TABLE registro_extension_aulica_version ADD COLUMN posee_centro_estudiantes boolean NULL;
ALTER TABLE registro_extension_aulica_version ADD COLUMN posee_representantes_estudiantiles boolean NULL;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('141', 'Registro', '#460');

COMMIT;
