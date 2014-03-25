BEGIN;

--
INSERT INTO seguridad_rol_credenciales (rol_id, credencial_id) VALUES
(
(SELECT id FROM seguridad_rol WHERE nombre = 'ReferenteJurisdiccional'), 
(SELECT id FROM seguridad_credencial WHERE nombre = 'validez_nacional_validez_index')
);

-------------------------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('127', 'Validez Nacional', 'RJ puede ver la validez de su jurisdicción - #386');

COMMIT;
