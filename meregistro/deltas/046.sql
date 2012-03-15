BEGIN;


INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_extension_aulica_modificar_pendiente', 'Edición los datos de una extensión áulica en estado Pendiente', 2, 'Extensiones Áulicas');

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_extension_aulica_ver', 'Ver Datos de Extensiones Áulicas', 2, 'Extensiones Áulicas');

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_extension_aulica_aprobar_registro', 'Aprobar Registro de Nuevo Extensión Áulica', 2, 'Extensiones Áulicas');

UPDATE seguridad_credencial SET descripcion = 'Solicitar Registro de Nuevo Extensión Áulica' WHERE nombre = 'reg_extension_aulica_alta';

UPDATE seguridad_credencial SET descripcion = 'Listar Extensiones Áulicas' WHERE nombre = 'reg_extension_aulica_consulta';
UPDATE seguridad_credencial SET descripcion = 'Eliminar Extensiones Áulicas' WHERE nombre = 'reg_extension_aulica_baja';
UPDATE seguridad_credencial SET descripcion = 'Cargar o Modificar Datos de Extensiones Áuliaas' WHERE nombre = 'reg_extension_aulica_modificar';



INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_aprobar_registro'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_aprobar_registro'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_aprobar_registro'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar_pendiente'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar_pendiente'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_modificar_pendiente'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_extension_aulica_consulta')
);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('046', 'Seguridad', 'Ticket #181');

COMMIT;

