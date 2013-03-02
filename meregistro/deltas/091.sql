BEGIN;

-------------------------------------

-- Table: titulos_estado_carrera
-- DROP TABLE titulos_estado_carrera;
CREATE TABLE titulos_estado_carrera
(
  id serial NOT NULL,
  nombre character varying(50) NOT NULL,
  CONSTRAINT titulos_estado_carrera_pkey PRIMARY KEY (id),
  CONSTRAINT titulos_estado_carrera_nombre_key UNIQUE (nombre)
)
WITH (
  OIDS=FALSE
);
  
-------------------------------------

-- Table: titulos_carrera
-- DROP TABLE titulos_carrera;

ALTER TABLE titulos_carrera ADD COLUMN estado_id integer NOT NULL;
ALTER TABLE titulos_carrera ADD COLUMN observaciones character varying(255);
ALTER TABLE titulos_carrera ADD COLUMN fecha_alta date NOT NULL;

ALTER TABLE titulos_carrera ADD CONSTRAINT titulos_carrera_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- Index: titulos_carrera_estado_id
-- DROP INDEX titulos_carrera_estado_id;
CREATE INDEX titulos_carrera_estado_id
  ON titulos_carrera
  USING btree
  (estado_id);
  
-------------------------------------
  
-- Table: titulos_carrera_estados
-- DROP TABLE titulos_carrera_estados;
CREATE TABLE titulos_carrera_estados
(
  id serial NOT NULL,
  carrera_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_carrera_estados_pkey PRIMARY KEY (id),
  CONSTRAINT titulos_carrera_estados_carrera_id_fkey FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carrera_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
-- Index: titulos_carrera_estados_carrera_id
-- DROP INDEX titulos_carrera_estados_carrera_id;
CREATE INDEX titulos_carrera_estados_carrera_id
  ON titulos_carrera_estados
  USING btree
  (carrera_id );
-- Index: titulos_carrera_estados_estado_id
-- DROP INDEX titulos_carrera_estados_estado_id;
CREATE INDEX titulos_carrera_estados_estado_id
  ON titulos_carrera_estados
  USING btree
  (estado_id );

-------------------------------------

-- Table: titulos_carreras_jurisdicciones
-- DROP TABLE titulos_carreras_jurisdicciones;
CREATE TABLE titulos_carreras_jurisdicciones
(
  id serial NOT NULL,
  carrera_id integer NOT NULL,
  jurisdiccion_id integer NOT NULL,
  CONSTRAINT titulos_carreras_jurisdicciones_pkey PRIMARY KEY (id),
  CONSTRAINT carrera_id_refs_id_6410b247 FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carreras_jurisdicciones_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id)
      REFERENCES registro_jurisdiccion (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carreras_jurisdicciones_carrera_id_jurisdiccion_id_key UNIQUE (carrera_id , jurisdiccion_id)
)
WITH (
  OIDS=FALSE
);
-- Index: titulos_carreras_jurisdicciones_carrera_id
-- DROP INDEX titulos_carreras_jurisdicciones_carrera_id;
CREATE INDEX titulos_carreras_jurisdicciones_carrera_id
  ON titulos_carreras_jurisdicciones
  USING btree
  (carrera_id );
-- Index: titulos_carreras_jurisdicciones_jurisdiccion_id
-- DROP INDEX titulos_carreras_jurisdicciones_jurisdiccion_id;
CREATE INDEX titulos_carreras_jurisdicciones_jurisdiccion_id
  ON titulos_carreras_jurisdicciones
  USING btree
  (jurisdiccion_id );


-------------------------------------

INSERT INTO titulos_estado_carrera (nombre) VALUES ('Vigente'), ('No vigente');

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('091', 'Titulos', 'Ticket #288');


COMMIT;
