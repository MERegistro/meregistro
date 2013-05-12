BEGIN;

ALTER TABLE consulta_validez_unidadeducativa ADD COLUMN dependencia_funcional_id integer;

-- Agrego las dependencias funcionales a establecimientos
UPDATE consulta_validez_unidadeducativa v
SET dependencia_funcional_id = (SELECT df.id 
	FROM registro_dependencia_funcional df
	INNER JOIN registro_establecimiento est ON est.dependencia_funcional_id = df.id
	WHERE est.cue = v.cue)
WHERE tipo_unidad_educativa = 'establecimiento';

-- Agrego las dependencias funcionales a anexos
UPDATE consulta_validez_unidadeducativa v
SET dependencia_funcional_id = (SELECT df.id 
	FROM registro_dependencia_funcional df
	INNER JOIN registro_establecimiento est ON est.dependencia_funcional_id = df.id
	INNER JOIN registro_anexo a ON a.establecimiento_id = est.id
	WHERE a.cue = v.cue)
WHERE tipo_unidad_educativa = 'anexo';

--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('103', 'ConsultaValidez', 'Ticket #308');

COMMIT;
