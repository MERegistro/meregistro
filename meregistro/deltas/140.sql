BEGIN;

-------------------------------------

-- Table: validez_nacional_informe_solicitud

-- DROP TABLE validez_nacional_informe_solicitud;

CREATE TABLE validez_nacional_informe_solicitud
(
  id serial NOT NULL,
  solicitud_id integer NOT NULL,
  normativa_implementacion boolean NOT NULL,
  disenio_jurisdiccional_unico boolean NOT NULL,
  denominacion_titulo boolean NOT NULL,
  carga_horaria_minima boolean NOT NULL,
  organizacion_estudios boolean NOT NULL,
  organizacion_tres_campos boolean NOT NULL,
  presencia_residencia_pedagogica boolean NOT NULL,
  acreditacion_condiciones_institucionales boolean NOT NULL,
  observaciones character varying(999),
  CONSTRAINT validez_nacional_informe_solicitud_pkey PRIMARY KEY (id),
  CONSTRAINT validez_nacional_informe_solicitud_solicitud_id_fkey FOREIGN KEY (solicitud_id)
      REFERENCES validez_nacional_solicitud (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: validez_nacional_informe_solicitud_solicitud_id

-- DROP INDEX validez_nacional_informe_solicitud_solicitud_id;

CREATE INDEX validez_nacional_informe_solicitud_solicitud_id
  ON validez_nacional_informe_solicitud
  USING btree
  (solicitud_id);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('140', 'Validez Nacional', 'Ticket #390');

COMMIT;
