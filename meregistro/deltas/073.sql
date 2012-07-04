BEGIN;

DROP TABLE registro_anexos_turnos;
DROP TABLE registro_anexos_turnos_version;

-- Table: registro_anexo_turno
-- DROP TABLE registro_anexo_turno;
CREATE TABLE registro_anexo_turno
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  turno_id integer NOT NULL,
  tipo_dominio_id integer,
  tipo_compartido_id integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_anexo_turno_pkey PRIMARY KEY (id),
  CONSTRAINT registro_anexo_turno_anexo_id_fkey FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_tipo_compartido_id_fkey FOREIGN KEY (tipo_compartido_id)
      REFERENCES registro_tipo_compartido (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_tipo_dominio_id_fkey FOREIGN KEY (tipo_dominio_id)
      REFERENCES registro_tipo_dominio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_turno_id_fkey FOREIGN KEY (turno_id)
      REFERENCES registro_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_anexo_id_turno_id_key UNIQUE (anexo_id, turno_id)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_anexo_turno_anexo_id
-- DROP INDEX registro_anexo_turno_anexo_id;
CREATE INDEX registro_anexo_turno_anexo_id
  ON registro_anexo_turno
  USING btree
  (anexo_id);
-- Index: registro_anexo_turno_tipo_compartido_id
-- DROP INDEX registro_anexo_turno_tipo_compartido_id;
CREATE INDEX registro_anexo_turno_tipo_compartido_id
  ON registro_anexo_turno
  USING btree
  (tipo_compartido_id);
-- Index: registro_anexo_turno_tipo_dominio_id
-- DROP INDEX registro_anexo_turno_tipo_dominio_id;
CREATE INDEX registro_anexo_turno_tipo_dominio_id
  ON registro_anexo_turno
  USING btree
  (tipo_dominio_id);
-- Index: registro_anexo_turno_turno_id
-- DROP INDEX registro_anexo_turno_turno_id;
CREATE INDEX registro_anexo_turno_turno_id
  ON registro_anexo_turno
  USING btree
  (turno_id);



-- Table: registro_anexo_turno_niveles
-- DROP TABLE registro_anexo_turno_niveles;
CREATE TABLE registro_anexo_turno_niveles
(
  id serial NOT NULL,
  anexoturno_id integer NOT NULL,
  nivel_id integer NOT NULL,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_anexo_turno_niveles_pkey PRIMARY KEY (id),
  CONSTRAINT anexoturno_id_refs_id_ee45e31e FOREIGN KEY (anexoturno_id)
      REFERENCES registro_anexo_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_niveles_nivel_id_fkey FOREIGN KEY (nivel_id)
      REFERENCES registro_nivel (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_anexo_turno_niveles_anexoturno_id_nivel_id_key UNIQUE (anexoturno_id, nivel_id)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_anexo_turno_niveles_anexoturno_id
-- DROP INDEX registro_anexo_turno_niveles_anexoturno_id;
CREATE INDEX registro_anexo_turno_niveles_anexoturno_id
  ON registro_anexo_turno_niveles
  USING btree
  (anexoturno_id);
-- Index: registro_anexo_turno_niveles_nivel_id
-- DROP INDEX registro_anexo_turno_niveles_nivel_id;
CREATE INDEX registro_anexo_turno_niveles_nivel_id
  ON registro_anexo_turno_niveles
  USING btree
  (nivel_id);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('073', 'Registro', 'Cambio en turnos -anexos- - Ticket #219');

COMMIT;
