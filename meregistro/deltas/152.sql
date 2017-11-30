BEGIN;


SELECT setval('public.registro_autoridad_cargo_id_seq', (SELECT MAX(id)+1 FROM registro_autoridad_cargo), true);
INSERT INTO registro_autoridad_cargo (descripcion) VALUES ('Secretario/a');
INSERT INTO registro_autoridad_cargo (descripcion) VALUES ('Coordinador/a');
INSERT INTO registro_autoridad_cargo (descripcion) VALUES ('Otro');

ALTER TABLE registro_establecimiento
ADD director_apellido character varying(40),
ADD director_nombre character varying(40),
ADD director_fecha_nacimiento date,
ADD director_tipo_documento_id integer,
ADD director_documento character varying(20),
ADD director_telefono character varying(30),
ADD director_celular character varying(30),
ADD director_email character varying(255)
;
ALTER TABLE registro_establecimiento
ADD CONSTRAINT registro_establecimiento_director_tipo_documento_id_fkey FOREIGN KEY (director_tipo_documento_id)
REFERENCES seguridad_tipo_documento (id) MATCH SIMPLE
ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;


UPDATE registro_establecimiento est
SET director_apellido = a.apellido, director_nombre = a.nombre, director_fecha_nacimiento = a.fecha_nacimiento, 
    director_tipo_documento_id = a.tipo_documento_id, director_documento = a.documento, director_telefono = a.telefono, 
    director_celular = a.celular, director_email = a.email
FROM registro_establecimiento_autoridades a
WHERE a.establecimiento_id = est.id;

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('152', 'Registro', 'Se agregan datos del director al establecimiento');

COMMIT;
