BEGIN;

DROP TABLE 
	titulos_titulo_jurisdiccional, 
	titulos_estado_titulo_jurisdiccional, 
	titulos_titulo_jurisd_cohorte,
	titulos_titulo_jurisd_estados,
	titulos_titulos_jurisd_normativas,
	titulos_titulos_jurisd_orientaciones,
	titulos_cohorte,
	titulos_egresados_anexo,
	titulos_egresados_establecimiento,
	titulos_egresados_establecimiento_detalle,
	titulos_egresados_anexo_detalle,
	titulos_cohortes_anexos,
	titulos_cohortes_establecimientos,
	titulos_cohortes_extensiones_aulicas,
	titulos_cohorte_extension_aulica_estados,
	titulos_cohorte_establecimiento_seguimiento,
	titulos_cohorte_establecimiento_estados,
	titulos_cohorte_anexo_estados,
	titulos_cohorte_anexo_seguimiento	
;
  
------------------------------------------------------------------------
  
-- Table: titulos_estado_carrera_jurisdiccional

-- DROP TABLE titulos_estado_carrera_jurisdiccional;

CREATE TABLE titulos_estado_carrera_jurisdiccional
(
  id serial NOT NULL,
  nombre character varying(50) NOT NULL,
  CONSTRAINT titulos_estado_carrera_jurisdiccional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_estado_carrera_jurisdiccional_nombre_key UNIQUE (nombre )
)
WITH (
  OIDS=FALSE
);

------------------------------------------------------------------------

-- Table: titulos_carrera_jurisdiccional

-- DROP TABLE titulos_carrera_jurisdiccional;

CREATE TABLE titulos_carrera_jurisdiccional
(
  id serial NOT NULL,
  carrera_id integer NOT NULL,
  jurisdiccion_id integer NOT NULL,
  estado_id integer NOT NULL,
  revisado_jurisdiccion boolean,
  CONSTRAINT titulos_carrera_jurisdiccional_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_carrera_jurisdiccional_carrera_id_fkey FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carrera_jurisdiccional_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carrera_jurisdiccional_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id)
      REFERENCES registro_jurisdiccion (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_carrera_jurisdiccional_carrera_id

-- DROP INDEX titulos_carrera_jurisdiccional_carrera_id;

CREATE INDEX titulos_carrera_jurisdiccional_carrera_id
  ON titulos_carrera_jurisdiccional
  USING btree
  (carrera_id );

-- Index: titulos_carrera_jurisdiccional_estado_id

-- DROP INDEX titulos_carrera_jurisdiccional_estado_id;

CREATE INDEX titulos_carrera_jurisdiccional_estado_id
  ON titulos_carrera_jurisdiccional
  USING btree
  (estado_id );

-- Index: titulos_carrera_jurisdiccional_jurisdiccion_id

-- DROP INDEX titulos_carrera_jurisdiccional_jurisdiccion_id;

CREATE INDEX titulos_carrera_jurisdiccional_jurisdiccion_id
  ON titulos_carrera_jurisdiccional
  USING btree
  (jurisdiccion_id );


------------------------------------------------------------------------

-- Table: titulos_carrera_jurisdiccional_cohorte

-- DROP TABLE titulos_carrera_jurisdiccional_cohorte;

CREATE TABLE titulos_carrera_jurisdiccional_cohorte
(
  id serial NOT NULL,
  carrera_jurisdiccional_id integer NOT NULL,
  primera_cohorte_solicitada integer NOT NULL,
  ultima_cohorte_solicitada integer NOT NULL,
  primera_cohorte_autorizada integer,
  ultima_cohorte_autorizada integer,
  observaciones character varying(255),
  CONSTRAINT titulos_carrera_jurisdiccional_cohorte_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_carrera_jurisdiccional_c_carrera_jurisdiccional_id_fkey FOREIGN KEY (carrera_jurisdiccional_id)
      REFERENCES titulos_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carrera_jurisdiccional__ultima_cohorte_autorizada_check CHECK (ultima_cohorte_autorizada >= 0),
  CONSTRAINT titulos_carrera_jurisdiccional__ultima_cohorte_solicitada_check CHECK (ultima_cohorte_solicitada >= 0),
  CONSTRAINT titulos_carrera_jurisdiccional_primera_cohorte_autorizada_check CHECK (primera_cohorte_autorizada >= 0),
  CONSTRAINT titulos_carrera_jurisdiccional_primera_cohorte_solicitada_check CHECK (primera_cohorte_solicitada >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_carrera_jurisdiccional_cohorte_carrera_jurisdiccionf9e8

-- DROP INDEX titulos_carrera_jurisdiccional_cohorte_carrera_jurisdiccionf9e8;

CREATE INDEX titulos_carrera_jurisdiccional_cohorte_carrera_jurisdiccionf9e8
  ON titulos_carrera_jurisdiccional_cohorte
  USING btree
  (carrera_jurisdiccional_id );

------------------------------------------------------------------------

-- Table: titulos_carrera_jurisdiccional_estados

-- DROP TABLE titulos_carrera_jurisdiccional_estados;

CREATE TABLE titulos_carrera_jurisdiccional_estados
(
  id serial NOT NULL,
  carrera_jurisdiccional_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_carrera_jurisdiccional_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_carrera_jurisdiccional_e_carrera_jurisdiccional_id_fkey FOREIGN KEY (carrera_jurisdiccional_id)
      REFERENCES titulos_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carrera_jurisdiccional_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_carrera_jurisdiccional_estados_carrera_jurisdiccion5657

-- DROP INDEX titulos_carrera_jurisdiccional_estados_carrera_jurisdiccion5657;

CREATE INDEX titulos_carrera_jurisdiccional_estados_carrera_jurisdiccion5657
  ON titulos_carrera_jurisdiccional_estados
  USING btree
  (carrera_jurisdiccional_id );

-- Index: titulos_carrera_jurisdiccional_estados_estado_id

-- DROP INDEX titulos_carrera_jurisdiccional_estados_estado_id;

CREATE INDEX titulos_carrera_jurisdiccional_estados_estado_id
  ON titulos_carrera_jurisdiccional_estados
  USING btree
  (estado_id );

------------------------------------------------------------------------

-- Table: titulos_carreras_jurisdiccionales_normativas

-- DROP TABLE titulos_carreras_jurisdiccionales_normativas;

CREATE TABLE titulos_carreras_jurisdiccionales_normativas
(
  id serial NOT NULL,
  carrerajurisdiccional_id integer NOT NULL,
  normativajurisdiccional_id integer NOT NULL,
  CONSTRAINT titulos_carreras_jurisdiccionales_normativas_pkey PRIMARY KEY (id ),
  CONSTRAINT carrerajurisdiccional_id_refs_id_94f743c5 FOREIGN KEY (carrerajurisdiccional_id)
      REFERENCES titulos_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carreras_jurisdiccional_normativajurisdiccional_id_fkey FOREIGN KEY (normativajurisdiccional_id)
      REFERENCES titulos_normativa_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_carreras_jurisdiccion_carrerajurisdiccional_id_norm_key UNIQUE (carrerajurisdiccional_id , normativajurisdiccional_id )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_carreras_jurisdiccionales_normativas_carrerajurisdi5316

-- DROP INDEX titulos_carreras_jurisdiccionales_normativas_carrerajurisdi5316;

CREATE INDEX titulos_carreras_jurisdiccionales_normativas_carrerajurisdi5316
  ON titulos_carreras_jurisdiccionales_normativas
  USING btree
  (carrerajurisdiccional_id );

-- Index: titulos_carreras_jurisdiccionales_normativas_normativajurisaba9

-- DROP INDEX titulos_carreras_jurisdiccionales_normativas_normativajurisaba9;

CREATE INDEX titulos_carreras_jurisdiccionales_normativas_normativajurisaba9
  ON titulos_carreras_jurisdiccionales_normativas
  USING btree
  (normativajurisdiccional_id );

------------------------------------------------------------------------

-- Table: titulos_cohorte

-- DROP TABLE titulos_cohorte;

CREATE TABLE titulos_cohorte
(
  id serial NOT NULL,
  carrera_jurisdiccional_id integer NOT NULL,
  anio integer NOT NULL,
  observaciones character varying(255),
  revisado_jurisdiccion boolean,
  CONSTRAINT titulos_cohorte_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_carrera_jurisdiccional_id_fkey FOREIGN KEY (carrera_jurisdiccional_id)
      REFERENCES titulos_carrera_jurisdiccional (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_carrera_jurisdiccional_id_anio_key UNIQUE (carrera_jurisdiccional_id , anio ),
  CONSTRAINT titulos_cohorte_anio_check CHECK (anio >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_carrera_jurisdiccional_id

-- DROP INDEX titulos_cohorte_carrera_jurisdiccional_id;

CREATE INDEX titulos_cohorte_carrera_jurisdiccional_id
  ON titulos_cohorte
  USING btree
  (carrera_jurisdiccional_id );

------------------------------------------------------------------------

-- Table: titulos_cohortes_anexos

-- DROP TABLE titulos_cohortes_anexos;

CREATE TABLE titulos_cohortes_anexos
(
  id serial NOT NULL,
  anexo_id integer NOT NULL,
  cohorte_id integer NOT NULL,
  oferta boolean,
  emite boolean,
  estado_id integer NOT NULL,
  CONSTRAINT titulos_cohortes_anexos_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohortes_anexos_anexo_id_fkey FOREIGN KEY (anexo_id)
      REFERENCES registro_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_anexos_cohorte_id_fkey FOREIGN KEY (cohorte_id)
      REFERENCES titulos_cohorte (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_anexos_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_anexos_anexo_id_cohorte_id_key UNIQUE (anexo_id , cohorte_id )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohortes_anexos_anexo_id

-- DROP INDEX titulos_cohortes_anexos_anexo_id;

CREATE INDEX titulos_cohortes_anexos_anexo_id
  ON titulos_cohortes_anexos
  USING btree
  (anexo_id );

-- Index: titulos_cohortes_anexos_cohorte_id

-- DROP INDEX titulos_cohortes_anexos_cohorte_id;

CREATE INDEX titulos_cohortes_anexos_cohorte_id
  ON titulos_cohortes_anexos
  USING btree
  (cohorte_id );

-- Index: titulos_cohortes_anexos_estado_id

-- DROP INDEX titulos_cohortes_anexos_estado_id;

CREATE INDEX titulos_cohortes_anexos_estado_id
  ON titulos_cohortes_anexos
  USING btree
  (estado_id );

------------------------------------------------------------------------

-- Table: titulos_cohorte_anexo_estados

-- DROP TABLE titulos_cohorte_anexo_estados;

CREATE TABLE titulos_cohorte_anexo_estados
(
  id serial NOT NULL,
  cohorte_anexo_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_cohorte_anexo_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_anexo_estados_cohorte_anexo_id_fkey FOREIGN KEY (cohorte_anexo_id)
      REFERENCES titulos_cohortes_anexos (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_anexo_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_anexo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_anexo_estados_cohorte_anexo_id

-- DROP INDEX titulos_cohorte_anexo_estados_cohorte_anexo_id;

CREATE INDEX titulos_cohorte_anexo_estados_cohorte_anexo_id
  ON titulos_cohorte_anexo_estados
  USING btree
  (cohorte_anexo_id );

-- Index: titulos_cohorte_anexo_estados_estado_id

-- DROP INDEX titulos_cohorte_anexo_estados_estado_id;

CREATE INDEX titulos_cohorte_anexo_estados_estado_id
  ON titulos_cohorte_anexo_estados
  USING btree
  (estado_id );

------------------------------------------------------------------------

-- Table: titulos_cohorte_anexo_seguimiento

-- DROP TABLE titulos_cohorte_anexo_seguimiento;

CREATE TABLE titulos_cohorte_anexo_seguimiento
(
  id serial NOT NULL,
  cohorte_anexo_id integer NOT NULL,
  anio integer NOT NULL,
  solo_cursan_nuevas_unidades integer NOT NULL,
  solo_recursan_nuevas_unidades integer NOT NULL,
  recursan_cursan_nuevas_unidades integer NOT NULL,
  no_cursan integer NOT NULL,
  egresados integer NOT NULL,
  observaciones character varying(255),
  CONSTRAINT titulos_cohorte_anexo_seguimiento_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_anexo_seguimiento_cohorte_anexo_id_fkey FOREIGN KEY (cohorte_anexo_id)
      REFERENCES titulos_cohortes_anexos (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_anexo_seguimiento_cohorte_anexo_id_anio_key UNIQUE (cohorte_anexo_id , anio ),
  CONSTRAINT titulos_cohorte_anexo_seguim_recursan_cursan_nuevas_unida_check CHECK (recursan_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_anexo_seguim_solo_recursan_nuevas_unidade_check CHECK (solo_recursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_anexo_seguimi_solo_cursan_nuevas_unidades_check CHECK (solo_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_anexo_seguimiento_anio_check CHECK (anio >= 0),
  CONSTRAINT titulos_cohorte_anexo_seguimiento_egresados_check CHECK (egresados >= 0),
  CONSTRAINT titulos_cohorte_anexo_seguimiento_no_cursan_check CHECK (no_cursan >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_anexo_seguimiento_cohorte_anexo_id

-- DROP INDEX titulos_cohorte_anexo_seguimiento_cohorte_anexo_id;

CREATE INDEX titulos_cohorte_anexo_seguimiento_cohorte_anexo_id
  ON titulos_cohorte_anexo_seguimiento
  USING btree
  (cohorte_anexo_id );


------------------------------------------------------------------------
 
-- Table: titulos_cohortes_establecimientos

-- DROP TABLE titulos_cohortes_establecimientos;

CREATE TABLE titulos_cohortes_establecimientos
(
  id serial NOT NULL,
  establecimiento_id integer NOT NULL,
  cohorte_id integer NOT NULL,
  oferta boolean,
  emite boolean,
  estado_id integer NOT NULL,
  CONSTRAINT titulos_cohortes_establecimientos_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohortes_establecimientos_cohorte_id_fkey FOREIGN KEY (cohorte_id)
      REFERENCES titulos_cohorte (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_establecimientos_establecimiento_id_fkey FOREIGN KEY (establecimiento_id)
      REFERENCES registro_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_establecimientos_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_establecimie_establecimiento_id_cohorte_id_key UNIQUE (establecimiento_id , cohorte_id )
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohortes_establecimientos_cohorte_id

-- DROP INDEX titulos_cohortes_establecimientos_cohorte_id;

CREATE INDEX titulos_cohortes_establecimientos_cohorte_id
  ON titulos_cohortes_establecimientos
  USING btree
  (cohorte_id );

-- Index: titulos_cohortes_establecimientos_establecimiento_id

-- DROP INDEX titulos_cohortes_establecimientos_establecimiento_id;

CREATE INDEX titulos_cohortes_establecimientos_establecimiento_id
  ON titulos_cohortes_establecimientos
  USING btree
  (establecimiento_id );

-- Index: titulos_cohortes_establecimientos_estado_id

-- DROP INDEX titulos_cohortes_establecimientos_estado_id;

CREATE INDEX titulos_cohortes_establecimientos_estado_id
  ON titulos_cohortes_establecimientos
  USING btree
  (estado_id );

------------------------------------------------------------------------

-- Table: titulos_cohorte_establecimiento_estados

-- DROP TABLE titulos_cohorte_establecimiento_estados;

CREATE TABLE titulos_cohorte_establecimiento_estados
(
  id serial NOT NULL,
  cohorte_establecimiento_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_cohorte_establecimiento_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_establecimiento_cohorte_establecimiento_id_fkey FOREIGN KEY (cohorte_establecimiento_id)
      REFERENCES titulos_cohortes_establecimientos (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_establecimiento_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_establecimiento (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_establecimiento_estados_cohorte_establecimi0442

-- DROP INDEX titulos_cohorte_establecimiento_estados_cohorte_establecimi0442;

CREATE INDEX titulos_cohorte_establecimiento_estados_cohorte_establecimi0442
  ON titulos_cohorte_establecimiento_estados
  USING btree
  (cohorte_establecimiento_id );

-- Index: titulos_cohorte_establecimiento_estados_estado_id

-- DROP INDEX titulos_cohorte_establecimiento_estados_estado_id;

CREATE INDEX titulos_cohorte_establecimiento_estados_estado_id
  ON titulos_cohorte_establecimiento_estados
  USING btree
  (estado_id );

------------------------------------------------------------------------

-- Table: titulos_cohorte_establecimiento_seguimiento

-- DROP TABLE titulos_cohorte_establecimiento_seguimiento;

CREATE TABLE titulos_cohorte_establecimiento_seguimiento
(
  id serial NOT NULL,
  cohorte_establecimiento_id integer NOT NULL,
  anio integer NOT NULL,
  solo_cursan_nuevas_unidades integer NOT NULL,
  solo_recursan_nuevas_unidades integer NOT NULL,
  recursan_cursan_nuevas_unidades integer NOT NULL,
  no_cursan integer NOT NULL,
  egresados integer NOT NULL,
  observaciones character varying(255),
  CONSTRAINT titulos_cohorte_establecimiento_seguimiento_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_establecimient_cohorte_establecimiento_id_fkey1 FOREIGN KEY (cohorte_establecimiento_id)
      REFERENCES titulos_cohortes_establecimientos (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_establecimien_cohorte_establecimiento_id_an_key UNIQUE (cohorte_establecimiento_id , anio ),
  CONSTRAINT titulos_cohorte_establecimie_recursan_cursan_nuevas_unida_check CHECK (recursan_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_establecimie_solo_recursan_nuevas_unidade_check CHECK (solo_recursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_establecimien_solo_cursan_nuevas_unidades_check CHECK (solo_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_establecimiento_seguimiento_anio_check CHECK (anio >= 0),
  CONSTRAINT titulos_cohorte_establecimiento_seguimiento_egresados_check CHECK (egresados >= 0),
  CONSTRAINT titulos_cohorte_establecimiento_seguimiento_no_cursan_check CHECK (no_cursan >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_establecimiento_seguimiento_cohorte_establebb4a

-- DROP INDEX titulos_cohorte_establecimiento_seguimiento_cohorte_establebb4a;

CREATE INDEX titulos_cohorte_establecimiento_seguimiento_cohorte_establebb4a
  ON titulos_cohorte_establecimiento_seguimiento
  USING btree
  (cohorte_establecimiento_id );

------------------------------------------------------------------------

-- Table: titulos_cohortes_extensiones_aulicas

-- DROP TABLE titulos_cohortes_extensiones_aulicas;

CREATE TABLE titulos_cohortes_extensiones_aulicas
(
  id serial NOT NULL,
  extension_aulica_id integer NOT NULL,
  cohorte_id integer NOT NULL,
  oferta boolean,
  estado_id integer NOT NULL,
  CONSTRAINT titulos_cohortes_extensiones_aulicas_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohortes_extensiones_aulicas_cohorte_id_fkey FOREIGN KEY (cohorte_id)
      REFERENCES titulos_cohorte (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_extensiones_aulicas_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_extensiones_aulicas_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id)
      REFERENCES registro_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohortes_extensiones__extension_aulica_id_cohorte_i_key UNIQUE (extension_aulica_id , cohorte_id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE titulos_cohortes_extensiones_aulicas
  OWNER TO luciano;

-- Index: titulos_cohortes_extensiones_aulicas_cohorte_id

-- DROP INDEX titulos_cohortes_extensiones_aulicas_cohorte_id;

CREATE INDEX titulos_cohortes_extensiones_aulicas_cohorte_id
  ON titulos_cohortes_extensiones_aulicas
  USING btree
  (cohorte_id );

-- Index: titulos_cohortes_extensiones_aulicas_estado_id

-- DROP INDEX titulos_cohortes_extensiones_aulicas_estado_id;

CREATE INDEX titulos_cohortes_extensiones_aulicas_estado_id
  ON titulos_cohortes_extensiones_aulicas
  USING btree
  (estado_id );

-- Index: titulos_cohortes_extensiones_aulicas_extension_aulica_id

-- DROP INDEX titulos_cohortes_extensiones_aulicas_extension_aulica_id;

CREATE INDEX titulos_cohortes_extensiones_aulicas_extension_aulica_id
  ON titulos_cohortes_extensiones_aulicas
  USING btree
  (extension_aulica_id );
  
------------------------------------------------------------------------

-- Table: titulos_cohorte_extension_aulica_estados

-- DROP TABLE titulos_cohorte_extension_aulica_estados;

CREATE TABLE titulos_cohorte_extension_aulica_estados
(
  id serial NOT NULL,
  cohorte_extension_aulica_id integer NOT NULL,
  estado_id integer NOT NULL,
  fecha date NOT NULL,
  CONSTRAINT titulos_cohorte_extension_aulica_estados_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_extension_auli_cohorte_extension_aulica_id_fkey FOREIGN KEY (cohorte_extension_aulica_id)
      REFERENCES titulos_cohortes_extensiones_aulicas (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_extension_aulica_estados_estado_id_fkey FOREIGN KEY (estado_id)
      REFERENCES titulos_estado_cohorte_extension_aulica (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_extension_aulica_estados_cohorte_extension_b659

-- DROP INDEX titulos_cohorte_extension_aulica_estados_cohorte_extension_b659;

CREATE INDEX titulos_cohorte_extension_aulica_estados_cohorte_extension_b659
  ON titulos_cohorte_extension_aulica_estados
  USING btree
  (cohorte_extension_aulica_id );

-- Index: titulos_cohorte_extension_aulica_estados_estado_id

-- DROP INDEX titulos_cohorte_extension_aulica_estados_estado_id;

CREATE INDEX titulos_cohorte_extension_aulica_estados_estado_id
  ON titulos_cohorte_extension_aulica_estados
  USING btree
  (estado_id );

-------------------------------------------------------

INSERT INTO titulos_estado_carrera_jurisdiccional (nombre) VALUES ('Sin controlar'), ('Controlado'), ('Registrado');

-------------------------------------------------------


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('099', 'Titulos', 'Avances en modificación de títulos jurisdiccionales a carreras jurisdiccionales');

COMMIT;
