BEGIN;

--------------
DELETE FROM seguridad_rol_credenciales 
WHERE rol_id IN (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteInstitucional') 
AND credencial_id IN (SELECT id FROM seguridad_credencial WHERE nombre = 'tit_titulo_consulta')
;

--------------

ALTER TABLE titulos_cohortes_establecimientos ADD COLUMN inscriptos INTEGER;
ALTER TABLE titulos_cohortes_establecimientos ADD CONSTRAINT titulos_cohortes_establecimientos_inscriptos_check CHECK (inscriptos >= 0);

--------------

ALTER TABLE titulos_cohortes_anexos ADD COLUMN inscriptos INTEGER;
ALTER TABLE titulos_cohortes_anexos ADD CONSTRAINT titulos_cohortes_anexos_inscriptos_check CHECK (inscriptos >= 0);

--------------

ALTER TABLE titulos_cohortes_extensiones_aulicas ADD COLUMN inscriptos INTEGER;
ALTER TABLE titulos_cohortes_extensiones_aulicas ADD CONSTRAINT titulos_cohortes_extensiones_aulicas_inscriptos_check CHECK (inscriptos >= 0);

---------------------------------------

-- Table: titulos_cohorte_extension_aulica_seguimiento
-- DROP TABLE titulos_cohorte_extension_aulica_seguimiento;

CREATE TABLE titulos_cohorte_extension_aulica_seguimiento
(
  id serial NOT NULL,
  cohorte_extension_aulica_id integer NOT NULL,
  anio integer NOT NULL,
  solo_cursan_nuevas_unidades integer NOT NULL,
  solo_recursan_nuevas_unidades integer NOT NULL,
  recursan_cursan_nuevas_unidades integer NOT NULL,
  no_cursan integer NOT NULL,
  egresados integer NOT NULL,
  observaciones character varying(255),
  CONSTRAINT titulos_cohorte_extension_aulica_seguimiento_pkey PRIMARY KEY (id ),
  CONSTRAINT titulos_cohorte_extension_aul_cohorte_extension_aulica_id_fkey1 FOREIGN KEY (cohorte_extension_aulica_id)
      REFERENCES titulos_cohortes_extensiones_aulicas (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT titulos_cohorte_extension_aul_cohorte_extension_aulica_id_a_key UNIQUE (cohorte_extension_aulica_id , anio ),
  CONSTRAINT titulos_cohorte_extension_au_recursan_cursan_nuevas_unida_check CHECK (recursan_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_extension_au_solo_recursan_nuevas_unidade_check CHECK (solo_recursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_extension_aul_solo_cursan_nuevas_unidades_check CHECK (solo_cursan_nuevas_unidades >= 0),
  CONSTRAINT titulos_cohorte_extension_aulica_seguimiento_anio_check CHECK (anio >= 0),
  CONSTRAINT titulos_cohorte_extension_aulica_seguimiento_egresados_check CHECK (egresados >= 0),
  CONSTRAINT titulos_cohorte_extension_aulica_seguimiento_no_cursan_check CHECK (no_cursan >= 0)
)
WITH (
  OIDS=FALSE
);

-- Index: titulos_cohorte_extension_aulica_seguimiento_cohorte_extensb97e
-- DROP INDEX titulos_cohorte_extension_aulica_seguimiento_cohorte_extensb97e;

CREATE INDEX titulos_cohorte_extension_aulica_seguimiento_cohorte_extensb97e
  ON titulos_cohorte_extension_aulica_seguimiento
  USING btree
  (cohorte_extension_aulica_id );

---------------------------------------


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('100', 'Títulos', 'Avances de seguimiento de cohorte - Ticket #300');

COMMIT;
