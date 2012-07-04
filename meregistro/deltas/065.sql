BEGIN;

UPDATE registro_tipo_dependencia_funcional SET nombre = 'Dirección de Educación Privada'
WHERE nombre = 'Municipal';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('065', 'Registro', '#206');

COMMIT;
