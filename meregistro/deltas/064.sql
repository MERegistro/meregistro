BEGIN;

UPDATE registro_tipo_dependencia_funcional SET nombre = 'Dirección de Educación Superior'
WHERE nombre = 'Dirección de Nivel Superior';

UPDATE registro_tipo_dependencia_funcional SET nombre = 'Municipal'
WHERE nombre = 'Dirección de Educación Privada';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('064', 'Registro', '#206');

COMMIT;
