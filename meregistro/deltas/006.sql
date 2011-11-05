-- Ticket #82

-- La agrego en la tabla establecimiento
ALTER TABLE registro_establecimiento
ADD COLUMN old_id integer unsigned NULL;

-- La agrego en la tabla anexo
ALTER TABLE registro_anexo
ADD COLUMN old_id integer unsigned NULL;

-- La agrego en la tabla unidad_extension
ALTER TABLE registro_unidad_extension
ADD COLUMN old_id integer unsigned NULL;
