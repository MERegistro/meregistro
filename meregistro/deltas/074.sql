BEGIN;

DROP TABLE registro_extensiones_aulicas_turnos;
DROP TABLE registro_extensiones_aulicas_turnos_version;

-- Table: registro_extension_aulica_turno
-- DROP TABLE registro_extension_aulica_turno;
CREATE TABLE registro_extension_aulica_turno
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  turno_id integer NOT NULL,
  tipo_dominio_id integer,
  tipo_compartido_id integer,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_extension_aulica_turno_pkey PRIMARY KEY (id),
  CONSTRAINT registro_extension_aulica_turno_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_turno_tipo_compartido_id_fkey FOREIGN KEY (tipo_compartido_id)
      REFERENCES registro_tipo_compartido (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_turno_tipo_dominio_id_fkey FOREIGN KEY (tipo_dominio_id)
      REFERENCES registro_tipo_dominio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_turno_turno_id_fkey FOREIGN KEY (turno_id)
      REFERENCES registro_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_turn_extension_aulica_id_turno_id_key UNIQUE (extension_aulica_id, turno_id)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_extension_aulica_turno_extension_aulica_id
-- DROP INDEX registro_extension_aulica_turno_extension_aulica_id;
CREATE INDEX registro_extension_aulica_turno_extension_aulica_id
  ON registro_extension_aulica_turno
  USING btree
  (extension_aulica_id);
-- Index: registro_extension_aulica_turno_tipo_compartido_id
-- DROP INDEX registro_extension_aulica_turno_tipo_compartido_id;
CREATE INDEX registro_extension_aulica_turno_tipo_compartido_id
  ON registro_extension_aulica_turno
  USING btree
  (tipo_compartido_id);
-- Index: registro_extension_aulica_turno_tipo_dominio_id
-- DROP INDEX registro_extension_aulica_turno_tipo_dominio_id;
CREATE INDEX registro_extension_aulica_turno_tipo_dominio_id
  ON registro_extension_aulica_turno
  USING btree
  (tipo_dominio_id);
-- Index: registro_extension_aulica_turno_turno_id
-- DROP INDEX registro_extension_aulica_turno_turno_id;
CREATE INDEX registro_extension_aulica_turno_turno_id
  ON registro_extension_aulica_turno
  USING btree
  (turno_id);


-- Table: registro_extension_aulica_turno_niveles
-- DROP TABLE registro_extension_aulica_turno_niveles;
CREATE TABLE registro_extension_aulica_turno_niveles
(
  id serial NOT NULL,
  extensionaulicaturno_id integer NOT NULL,
  nivel_id integer NOT NULL,
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT registro_extension_aulica_turno_niveles_pkey PRIMARY KEY (id),
  CONSTRAINT extensionaulicaturno_id_refs_id_3d756778 FOREIGN KEY (extensionaulicaturno_id)
      REFERENCES registro_extension_aulica_turno (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_turno_niveles_nivel_id_fkey FOREIGN KEY (nivel_id)
      REFERENCES registro_nivel (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT registro_extension_aulica_tur_extensionaulicaturno_id_nivel_key UNIQUE (extensionaulicaturno_id, nivel_id)
)
WITH (
  OIDS=FALSE
);
-- Index: registro_extension_aulica_turno_niveles_extensionaulicaturno_id
-- DROP INDEX registro_extension_aulica_turno_niveles_extensionaulicaturno_id;
CREATE INDEX registro_extension_aulica_turno_niveles_extensionaulicaturno_id
  ON registro_extension_aulica_turno_niveles
  USING btree
  (extensionaulicaturno_id);
-- Index: registro_extension_aulica_turno_niveles_nivel_id
-- DROP INDEX registro_extension_aulica_turno_niveles_nivel_id;
CREATE INDEX registro_extension_aulica_turno_niveles_nivel_id
  ON registro_extension_aulica_turno_niveles
  USING btree
  (nivel_id);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('074', 'Registro', 'Cambio en turnos -extensiones áulicas- - Ticket #219');

COMMIT;
