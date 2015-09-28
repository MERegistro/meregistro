BEGIN;

-- Table: postitulos_informe_solicitud

-- DROP TABLE postitulos_informe_solicitud;

CREATE TABLE postitulos_informe_solicitud
(
  id serial NOT NULL,
  solicitud_id integer NOT NULL,
  denominacion_titulo boolean NOT NULL,
  observaciones character varying(999),
  CONSTRAINT postitulos_informe_solicitud_pkey PRIMARY KEY (id),
  CONSTRAINT postitulos_informe_solicitud_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES postitulos_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: postitulos_informe_solicitud_solicitud_id

-- DROP INDEX postitulos_informe_solicitud_solicitud_id;

CREATE INDEX postitulos_informe_solicitud_solicitud_id
  ON postitulos_informe_solicitud
  USING btree
  (solicitud_id);

---------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('146', 'Postítulos', '#484');

COMMIT;
