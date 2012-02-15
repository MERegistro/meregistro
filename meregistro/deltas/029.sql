BEGIN;

INSERT INTO registro_tipo_dependencia_funcional (nombre) VALUES ('Dependencia Temporal');

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('029', 'Registro', 'Ticket #155');

COMMIT;
