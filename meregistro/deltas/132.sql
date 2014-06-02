BEGIN;

--
INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES ('Postítulos', 'Postítulos', '/postitulos/');

-- SCHEMA DUMP ACA

-----------------------
INSERT INTO postitulos_estado_carrera_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_carrera_postitulo_jurisdiccional (nombre) VALUES ('Sin controlar'), ('Controlado'), ('Registrado');
INSERT INTO postitulos_estado_postitulo_nacional (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_normativa_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_normativa_postitulo_jurisdiccional (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_normativa_motivo_otorgamiento (nombre) VALUES ('Aprobación'), ('Implementación'), ('Aprobación/Implementación');
INSERT INTO postitulos_tipo_normativa_postitulo_jurisdiccional (nombre) VALUES ('Resolución'), ('Decreto'), ('Disposición'), ('Actuación'), ('Acuerdo'), ('Circular');
INSERT INTO postitulos_estado_solicitud (nombre) VALUES ('Controlado'), ('Numerado'), ('Pendiente');


-----------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('132', 'Postítulos', 'Aplicación de postítulos - #406');

COMMIT;
