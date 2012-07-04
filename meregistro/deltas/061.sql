BEGIN;
--
--
-- Sedes
INSERT INTO registro_establecimiento_domicilio (establecimiento_id, tipo_domicilio_id, localidad_id, calle, altura, referencia, cp, last_user_id, created_at, updated_at)
(SELECT establecimiento_id, 2, localidad_id, calle, altura, referencia, cp, last_user_id, NOW(), NOW() FROM registro_establecimiento_domicilio);

-- Anexos
INSERT INTO registro_anexo_domicilio (anexo_id, tipo_domicilio_id, localidad_id, calle, altura, referencia, cp, last_user_id, created_at, updated_at)
(SELECT anexo_id, 2, localidad_id, calle, altura, referencia, cp, last_user_id, NOW(), NOW() FROM registro_anexo_domicilio);

-- Extensiones áulicas
INSERT INTO registro_extension_aulica_domicilio (extension_aulica_id, tipo_domicilio_id, localidad_id, calle, altura, referencia, cp, last_user_id, created_at, updated_at)
(SELECT extension_aulica_id, 2, localidad_id, calle, altura, referencia, cp, last_user_id, NOW(), NOW() FROM registro_extension_aulica_domicilio);

--
--
INSERT INTO deltas_sql (numero, app, comentario) VALUES ('061', 'Registro', 'Duplicar domicilios - Ticket #214');

COMMIT;
