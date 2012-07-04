BEGIN;


DELETE FROM seguridad_ambito WHERE id not IN

(SELECT ambito_id FROM registro_dependencia_funcional
UNION
SELECT ambito_id FROM registro_anexo
UNION
SELECT ambito_id FROM registro_establecimiento
UNION
SELECT ambito_id FROM registro_extension_aulica
UNION
SELECT ambito_id FROM registro_jurisdiccion)
AND level > 0;

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('058', 'Registro', '#205');

COMMIT;
