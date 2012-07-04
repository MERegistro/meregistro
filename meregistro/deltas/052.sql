-- Preparar tablas para migración
BEGIN;

--
-- Establecimientos
ALTER TABLE registro_establecimiento ALTER COLUMN norma_creacion DROP NOT NULL;
ALTER TABLE registro_establecimiento_version ALTER COLUMN norma_creacion DROP NOT NULL;

-- Domicilios de establecimiento
ALTER TABLE registro_establecimiento_domicilio ALTER COLUMN altura DROP NOT NULL;
ALTER TABLE registro_establecimiento_domicilio_version ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_establecimiento_domicilio ALTER COLUMN cp DROP NOT NULL;
ALTER TABLE registro_establecimiento_domicilio_version ALTER COLUMN cp DROP NOT NULL;

ALTER TABLE registro_establecimiento_domicilio ALTER COLUMN calle DROP NOT NULL;
ALTER TABLE registro_establecimiento_domicilio_version ALTER COLUMN calle DROP NOT NULL;

--
-- Anexos
ALTER TABLE registro_anexo ALTER COLUMN norma_creacion DROP NOT NULL;
ALTER TABLE registro_anexo_version ALTER COLUMN norma_creacion DROP NOT NULL;

-- Domicilios de anexo
ALTER TABLE registro_anexo_domicilio ALTER COLUMN altura DROP NOT NULL;
ALTER TABLE registro_anexo_domicilio_version ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_anexo_domicilio ALTER COLUMN cp DROP NOT NULL;
ALTER TABLE registro_anexo_domicilio_version ALTER COLUMN cp DROP NOT NULL;

ALTER TABLE registro_anexo_domicilio ALTER COLUMN calle DROP NOT NULL;
ALTER TABLE registro_anexo_domicilio_version ALTER COLUMN calle DROP NOT NULL;

--
-- Extensiones áulicas
ALTER TABLE registro_extension_aulica ALTER COLUMN observaciones DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN observaciones DROP NOT NULL;

ALTER TABLE registro_extension_aulica ALTER COLUMN norma_creacion DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN norma_creacion DROP NOT NULL;

ALTER TABLE registro_extension_aulica ALTER COLUMN norma_creacion_numero DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN norma_creacion_numero DROP NOT NULL;

ALTER TABLE registro_extension_aulica ALTER COLUMN origen_norma_id DROP NOT NULL;
ALTER TABLE registro_extension_aulica_version ALTER COLUMN origen_norma_id DROP NOT NULL;

-- Domicilios de extensión áulica
ALTER TABLE registro_extension_aulica_domicilio ALTER COLUMN calle DROP NOT NULL;
ALTER TABLE registro_extension_aulica_domicilio_version ALTER COLUMN calle DROP NOT NULL;

ALTER TABLE registro_extension_aulica_domicilio ALTER COLUMN altura DROP NOT NULL;
ALTER TABLE registro_extension_aulica_domicilio_version ALTER COLUMN altura DROP NOT NULL;

ALTER TABLE registro_extension_aulica_domicilio ALTER COLUMN cp DROP NOT NULL;
ALTER TABLE registro_extension_aulica_domicilio_version ALTER COLUMN cp DROP NOT NULL;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('052', 'Registro', 'Cambios en las tablas necesarios para poder realizar la migración');

COMMIT;
