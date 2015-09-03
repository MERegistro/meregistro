BEGIN;


--- Se agrega un nuevo tipo de gestión

INSERT INTO registro_tipo_gestion (nombre) VALUES ('Social');

---------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('145', 'Registro', '#481');

COMMIT;
