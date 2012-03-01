BEGIN;

DELETE FROM seguridad_rol_credenciales WHERE credencial_id IN
(
    SELECT id FROM seguridad_credencial WHERE nombre IN
    (
        'reportes_listado_usuarios'
    )
);

DELETE FROM seguridad_credencial WHERE nombre IN
(
    'reportes_listado_usuarios'
);

INSERT INTO seguridad_credencial (nombre, descripcion, aplicacion_id, grupo) VALUES
('seg_usuario_eliminar', 'Baja de Usuarios', 1, 'Seguridad y Usuarios');

UPDATE seguridad_credencial SET descripcion = 'Listar Usuarios' WHERE nombre = 'seg_usuario_buscar';
UPDATE seguridad_credencial SET descripcion = 'Registrar Roles y Credenciales' WHERE nombre = 'seg_rol_registrar';
UPDATE seguridad_credencial SET descripcion = 'Alta Nuevo Usuario' WHERE nombre = 'seg_usuario_alta';


INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_buscar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_buscar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_bloquear'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_bloquear'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_bloquear')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_buscar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_bloquear')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_buscar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_bloquear')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_buscar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_perfil_asignar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_eliminar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_rol_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'seg_usuario_alta')
)
;


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('037', 'Seguridad', 'Ticket #166');

COMMIT;

