BEGIN;

-- Baja -> No vigente
UPDATE registro_registro_establecimiento
SET estado_id = (
	SELECT id FROM registro_estado_establecimiento WHERE nombre = 'No vigente'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_establecimiento WHERE nombre = 'Baja'
);
--
UPDATE registro_anexo_estados
SET estado_id = (
	SELECT id FROM registro_estado_anexo WHERE nombre = 'No vigente'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_anexo WHERE nombre = 'Baja'
);
--
UPDATE registro_extension_aulica_estados
SET estado_id = (
	SELECT id FROM registro_estado_extension_aulica WHERE nombre = 'No vigente'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_extension_aulica WHERE nombre = 'Baja'
);
-- Vigente -> Registrado
UPDATE registro_registro_establecimiento
SET estado_id = (
	SELECT id FROM registro_estado_establecimiento WHERE nombre = 'Registrado'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_establecimiento WHERE nombre = 'Vigente'
);
--
UPDATE registro_anexo_estados
SET estado_id = (
	SELECT id FROM registro_estado_anexo WHERE nombre = 'Registrado'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_anexo WHERE nombre = 'Vigente'
);
--
UPDATE registro_extension_aulica_estados
SET estado_id = (
	SELECT id FROM registro_estado_extension_aulica WHERE nombre = 'Registrada'
)
WHERE estado_id = (
	SELECT id FROM registro_estado_extension_aulica WHERE nombre = 'Vigente'
);
--
--
DELETE FROM registro_estado_establecimiento WHERE nombre IN('Baja', 'Vigente');
--
DELETE FROM registro_estado_anexo WHERE nombre IN('Baja', 'Vigente');
--
DELETE FROM registro_estado_extension_aulica WHERE nombre IN('Baja', 'Vigente');
--

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('122', 'Registro', 'Estados de UEs - Ticket #359');

COMMIT;

