BEGIN;

DROP TABLE registro_establecimientos_turnos;
DROP TABLE registro_establecimientos_turnos_version;

-- Table: registro_establecimiento_turno
-- DROP TABLE registro_establecimiento_turno;
CREATE TABLE registro_establecimiento_turno
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  turno_id integer NOT NULL,
  tipo_dominio_id integer,
  tipo_compartido_id integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_establecimiento_turno_pkey PRIMARY KEY (id),
  CONSTRAINT registro_establecimiento_turno_establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_turno_tipo_compartido_id_fkey FOREIGN KEY (tipo_compartido_id)
      REFERENCES registro_tipo_compartido (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_turno_tipo_dominio_id_fkey FOREIGN KEY (tipo_dominio_id)
      REFERENCES registro_tipo_dominio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_turno_turno_id_fkey FOREIGN KEY (turno_id)
      REFERENCES registro_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("establecimiento_id", "turno_id")
)
WITH (
  OIDS=FALSE
);
-- Index: registro_establecimiento_turno_establecimiento_id
-- DROP INDEX registro_establecimiento_turno_establecimiento_id;
CREATE INDEX registro_establecimiento_turno_establecimiento_id
  ON registro_establecimiento_turno
  USING btree
  (establecimiento_id);
-- Index: registro_establecimiento_turno_tipo_compartido_id
-- DROP INDEX registro_establecimiento_turno_tipo_compartido_id;
CREATE INDEX registro_establecimiento_turno_tipo_compartido_id
  ON registro_establecimiento_turno
  USING btree
  (tipo_compartido_id);
-- Index: registro_establecimiento_turno_tipo_dominio_id
-- DROP INDEX registro_establecimiento_turno_tipo_dominio_id;
CREATE INDEX registro_establecimiento_turno_tipo_dominio_id
  ON registro_establecimiento_turno
  USING btree
  (tipo_dominio_id);
-- Index: registro_establecimiento_turno_turno_id
-- DROP INDEX registro_establecimiento_turno_turno_id;
CREATE INDEX registro_establecimiento_turno_turno_id
  ON registro_establecimiento_turno
  USING btree
  (turno_id);



-- Table: registro_establecimiento_turno_niveles
-- DROP TABLE registro_establecimiento_turno_niveles;
CREATE TABLE registro_establecimiento_turno_niveles
(
  id serial NOT NULL,
  establecimientoturno_id integer NOT NULL,
  nivel_id integer NOT NULL,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_establecimiento_turno_niveles_pkey PRIMARY KEY (id),
  CONSTRAINT establecimientoturno_id_refs_id_c304013c FOREIGN KEY (establecimientoturno_id)
      REFERENCES registro_establecimiento_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_turno_niveles_nivel_id_fkey FOREIGN KEY (nivel_id)
      REFERENCES registro_nivel (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_establecimiento_turn_establecimientoturno_id_nivel_key UNIQUE (establecimientoturno_id, nivel_id)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_establecimiento_turno_niveles_establecimientoturno_id
-- DROP INDEX registro_establecimiento_turno_niveles_establecimientoturno_id;
CREATE INDEX registro_establecimiento_turno_niveles_establecimientoturno_id
  ON registro_establecimiento_turno_niveles
  USING btree
  (establecimientoturno_id);
-- Index: registro_establecimiento_turno_niveles_nivel_id
-- DROP INDEX registro_establecimiento_turno_niveles_nivel_id;
CREATE INDEX registro_establecimiento_turno_niveles_nivel_id
  ON registro_establecimiento_turno_niveles
  USING btree
  (nivel_id);
--

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('072', 'Registro', 'Cambio en turnos - Ticket #219');

COMMIT;
