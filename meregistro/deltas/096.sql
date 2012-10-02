BEGIN;

UPDATE seguridad_credencial 
SET nombre = 'tit_carrera_jurisdiccional_alta',
descripcion = 'Alta de nueva carrera jurisdiccional'
WHERE nombre = 'tit_titulo_jurisdiccional_alta';

UPDATE seguridad_credencial 
SET nombre = 'tit_carrera_jurisdiccional_modificar',
descripcion = 'Modificar datos de carrera jurisdiccional'
WHERE nombre = 'tit_titulo_jurisdiccional_modificar';

UPDATE seguridad_credencial 
SET nombre = 'tit_carrera_jurisdiccional_consulta',
descripcion = 'Consultar datos de carreras jurisdiccionales'
WHERE nombre = 'tit_titulo_jurisdiccional_consulta';

UPDATE seguridad_credencial 
SET nombre = 'tit_carrera_jurisdiccional_eliminar',
descripcion = 'Eliminar carrera jurisdiccional'
WHERE nombre = 'tit_titulo_jurisdiccional_eliminar';

ALTER TABLE titulos_titulo_jurisdiccional DROP CONSTRAINT titulos_titulo_jurisdiccional_titulo_id_fkey;

ALTER TABLE titulos_titulo_jurisdiccional RENAME titulo_id  TO carrera_id;

ALTER TABLE titulos_titulo_jurisdiccional
  ADD CONSTRAINT titulos_titulo_jurisdiccional_carrera_id_fkey FOREIGN KEY (carrera_id)
      REFERENCES titulos_carrera (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('096', 'Titulos', 'Ticket #297');

COMMIT;
