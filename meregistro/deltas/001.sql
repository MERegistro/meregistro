BEGIN;
-- Table: deltas_sql

-- DROP TABLE deltas_sql;

CREATE TABLE deltas_sql
(
  id serial PRIMARY KEY,
  numero varchar(4) NOT NULL UNIQUE,
  app varchar(20) NOT NULL,
  comentario varchar(255) NULL,
  fecha_ejecucion date default CURRENT_DATE
)
WITH (
  OIDS=FALSE
);

insert into deltas_sql (numero, app, comentario) values ('001', 'Registro', 'Creación de la tabla que contiene el registro de deltas ejecutados.');
COMMIT;