BEGIN;

-- Agregar cues a ambitos de establecimientos
UPDATE seguridad_ambito a
SET descripcion = est.cue || ' - ' || descripcion
FROM registro_establecimiento est 
WHERE a.id = est.ambito_id 
AND a.tipo_id = 4;

-- Agregar cues a ambitos de anexos
UPDATE seguridad_ambito a
SET descripcion = anexo.cue || ' - ' || descripcion
FROM registro_anexo anexo 
WHERE a.id = anexo.ambito_id 
AND a.tipo_id = 5;

-- Agregar cues a ambitos de extensiones áulicas
UPDATE seguridad_ambito a
SET descripcion = ea.cue || ' - ' || descripcion
FROM registro_extension_aulica ea 
WHERE a.id = ea.ambito_id 
AND a.tipo_id = 6;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('123', 'Registro', 'CUE en descripción de ámbito de UE - Ticket #376');

COMMIT;
