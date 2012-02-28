BEGIN;

DELETE FROM seguridad_rol_credenciales WHERE credencial_id IN
(
    SELECT id FROM seguridad_credencial WHERE nombre IN
    (
        'reg_anexo_modificar'
    )
);

DELETE FROM seguridad_credencial WHERE nombre IN
(
    'reg_anexo_modificar'
);

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_anexo_aprobar_registro', 'Aprobar Registro de Nuevo Anexo', 2, 'Anexos');

UPDATE seguridad_credencial SET descripcion = 'Solicitar Registro de Nuevo Anexo' WHERE nombre = 'reg_anexo_alta';

UPDATE seguridad_credencial SET descripcion = 'Listar Anexos' WHERE nombre = 'reg_anexo_consulta';
UPDATE seguridad_credencial SET descripcion = 'Eliminar Anexos' WHERE nombre = 'reg_anexo_baja';
UPDATE seguridad_credencial SET descripcion = 'Cargar o Modificar Datos de Anexos' WHERE nombre = 'reg_anexo_completar';

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('reg_anexo_ver', 'Ver Datos de Anexos', 2, 'Anexos');


INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_ver'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_completar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_anexo_ver')
);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('036', 'Seguridad', 'Ticket #164');

COMMIT;

