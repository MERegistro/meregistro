BEGIN;

UPDATE seguridad_rol SET
padre_id = (SELECT id FROM seguridad_rol WHERE nombre = 'AdminSeguridad')
WHERE nombre = 'AdminNacional';

UPDATE seguridad_rol SET
padre_id = (SELECT id FROM seguridad_rol WHERE nombre = 'AdminNacional')
WHERE nombre = 'ReferenteJurisdiccional';

UPDATE seguridad_rol SET
padre_id = (SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional')
WHERE nombre = 'ReferenteInstitucional';


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('085h', 'Seguridad', '#303 hotfix');


COMMIT;
