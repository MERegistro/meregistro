-- AdminTitulos / ver establecimientos
insert into seguridad_rol_credenciales (rol_id, credencial_id)
  select rol.id as rol_id, cred.id as credencial_id
  from seguridad_rol rol, seguridad_credencial cred
  where rol.nombre = 'AdminTitulos'
  and cred.nombre = 'reg_establecimiento_ver'
;

-- Referente / ver establecimientos
insert into seguridad_rol_credenciales (rol_id, credencial_id)
  select rol.id as rol_id, cred.id as credencial_id
  from seguridad_rol rol, seguridad_credencial cred
  where rol.nombre = 'Referente'
  and cred.nombre = 'reg_establecimiento_ver'
;

-- Rector/director / ver establecimientos
insert into seguridad_rol_credenciales (rol_id, credencial_id)
  select rol.id as rol_id, cred.id as credencial_id
  from seguridad_rol rol, seguridad_credencial cred
  where rol.nombre = 'RectorDirectorIFD'
  and cred.nombre = 'reg_establecimiento_ver'
;
