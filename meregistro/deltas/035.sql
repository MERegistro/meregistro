BEGIN;

DELETE FROM seguridad_rol_credenciales WHERE credencial_id IN
(
    SELECT id FROM seguridad_credencial WHERE nombre IN
    (
        'reg_establecimiento_autoridad_consulta',
        'reg_establecimiento_autoridad_create',
        'reg_establecimiento_autoridad_delete',
        'reg_establecimiento_autoridad_edit',
        'reg_establecimiento_modificar'
    )
);

DELETE FROM seguridad_credencial WHERE nombre IN
(
    'reg_establecimiento_autoridad_consulta',
    'reg_establecimiento_autoridad_create',
    'reg_establecimiento_autoridad_delete',
    'reg_establecimiento_autoridad_edit',
    'reg_establecimiento_modificar'
);

UPDATE seguridad_credencial SET descripcion = 'Listar Sedes' WHERE nombre = 'reg_establecimiento_consulta';

UPDATE seguridad_credencial SET descripcion = 'Solicitar Registro de Nueva Sede' WHERE nombre = 'reg_establecimiento_nueva';
UPDATE seguridad_credencial SET descripcion = 'Aprobar Registro de Nueva Sede' WHERE nombre = 'reg_establecimiento_registrar';
UPDATE seguridad_credencial SET descripcion = 'Eliminar Sedes' WHERE nombre = 'reg_establecimiento_baja';
UPDATE seguridad_credencial SET descripcion = 'Cargar o Modificar Datos de Sedes' WHERE nombre = 'reg_establecimiento_completar';
UPDATE seguridad_credencial SET descripcion = 'Ver Datos de Sedes' WHERE nombre = 'reg_establecimiento_ver';



INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_nueva'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_nueva'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_nueva'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_completar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_nueva'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_registrar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_establecimiento_ver')
);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('035', 'Seguridad', 'Ticket #163');

COMMIT;

