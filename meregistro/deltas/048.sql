BEGIN;

TRUNCATE registro_turno RESTART IDENTITY CASCADE;

INSERT INTO registro_turno (nombre) VALUES
('Mañana'), ('Tarde'), ('Noche');

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('048', 'Registro', '#187');

COMMIT;
