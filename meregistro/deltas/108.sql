BEGIN;
-------------------------------------

-- Table: validez_nacional_solicitud_establecimientos
-- DROP TABLE validez_nacional_solicitud_establecimientos;
CREATE TABLE validez_nacional_solicitud_establecimientos
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  solicitud_id integer NOT NULL,
  CONSTRAINT validez_nacional_solicitud_establecimientos_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_solicitud_establecimie_establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_establecimientos_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_es_establecimiento_id_solicitud__key UNIQUE (establecimiento_id, solicitud_id)
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_solicitud_establecimientos_establecimiento_id
-- DROP INDEX validez_nacional_solicitud_establecimientos_establecimiento_id;
CREATE INDEX validez_nacional_solicitud_establecimientos_establecimiento_id
  ON validez_nacional_solicitud_establecimientos
  USING btree
  (establecimiento_id);

-- Index: validez_nacional_solicitud_establecimientos_solicitud_id
-- DROP INDEX validez_nacional_solicitud_establecimientos_solicitud_id;
CREATE INDEX validez_nacional_solicitud_establecimientos_solicitud_id
  ON validez_nacional_solicitud_establecimientos
  USING btree
  (solicitud_id);

-------------------------------------

-- Table: validez_nacional_solicitud_anexos
-- DROP TABLE validez_nacional_solicitud_anexos;
CREATE TABLE validez_nacional_solicitud_anexos
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  solicitud_id integer NOT NULL,
  CONSTRAINT validez_nacional_solicitud_anexos_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_solicitud_anexos_anexo_id_fkey FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_anexos_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT validez_nacional_solicitud_anexos_anexo_id_solicitud_id_key UNIQUE (anexo_id, solicitud_id)
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_solicitud_anexos_anexo_id
-- DROP INDEX validez_nacional_solicitud_anexos_anexo_id;
CREATE INDEX validez_nacional_solicitud_anexos_anexo_id
  ON validez_nacional_solicitud_anexos
  USING btree
  (anexo_id);

-- Index: validez_nacional_solicitud_anexos_solicitud_id
-- DROP INDEX validez_nacional_solicitud_anexos_solicitud_id;
CREATE INDEX validez_nacional_solicitud_anexos_solicitud_id
  ON validez_nacional_solicitud_anexos
  USING btree
  (solicitud_id);

-------------------------------------
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('108', 'Validez Nacional', 'Avances Ticket #322');

COMMIT;
