BEGIN;


ALTER TABLE registro_establecimiento
ADD director_apellido character varying(40),
ADD director_nombre character varying(40),
ADD director_fecha_nacimiento date,
ADD director_cargo_id integer,
ADD director_tipo_documento_id integer,
ADD director_documento character varying(20),
ADD director_telefono character varying(30),
ADD director_celular character varying(30),
ADD director_email character varying(255)
;

ALTER TABLE registro_establecimiento
ADD CONSTRAINT registro_establecimiento_director_cargo_id_fkey FOREIGN KEY (director_cargo_id)
REFERENCES registro_autoridad_cargo (id) MATCH SIMPLE
ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE registro_establecimiento
ADD CONSTRAINT registro_establecimiento_director_tipo_documento_id_fkey FOREIGN KEY (director_tipo_documento_id)
REFERENCES seguridad_tipo_documento (id) MATCH SIMPLE
ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;



-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('152', 'Registro', '');

COMMIT;
