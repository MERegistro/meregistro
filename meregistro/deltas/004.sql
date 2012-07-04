BEGIN;

INSERT INTO seguridad_rol_roles_asignables (from_rol_id, to_rol_id)
VALUES (
  (SELECT id FROM seguridad_rol WHERE nombre = 'Referente'),
  (SELECT id FROM seguridad_rol WHERE nombre = 'RectorDirectorIFD')
);

DELETE FROM seguridad_rol_roles_asignables t1 WHERE EXISTS
( SELECT 1 FROM seguridad_rol_roles_asignables t2 
  WHERE t2.from_rol_id = t1.from_rol_id AND t2.to_rol_id = t1.to_rol_id AND t1.id < t2.id
);

insert into deltas_sql (numero, app, comentario) values ('004', 'Seguridad', 'Correcion de roles asignables.');

COMMIT;
