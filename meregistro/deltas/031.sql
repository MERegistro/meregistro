-- Eliminar los ámbitos de anexos, establecimientos y dependencias.
-- Eliminar los perfiles con esos ámbitos

BEGIN;

DELETE FROM seguridad_perfil
WHERE ambito_id IN (SELECT ambito_id FROM registro_anexo)
OR ambito_id IN (SELECT ambito_id FROM registro_extension_aulica)
OR ambito_id IN (SELECT ambito_id FROM registro_establecimiento)
OR ambito_id IN (SELECT ambito_id FROM registro_dependencia_funcional);

DELETE FROM seguridad_perfil_version
WHERE ambito_id IN (SELECT ambito_id FROM registro_anexo)
OR ambito_id IN (SELECT ambito_id FROM registro_extension_aulica)
OR ambito_id IN (SELECT ambito_id FROM registro_establecimiento)
OR ambito_id IN (SELECT ambito_id FROM registro_dependencia_funcional);


-- Ámbitos
DELETE FROM seguridad_ambito  
WHERE id NOT IN
	(SELECT ambito_id FROM registro_anexo 
	UNION SELECT ambito_id FROM registro_establecimiento  
	UNION SELECT ambito_id FROM registro_dependencia_funcional  
	UNION SELECT ambito_id FROM registro_jurisdiccion)
AND level > 0;

TRUNCATE
	registro_anexo_baja,
	registro_anexo_conexion_internet,
	registro_anexo_conexion_internet_version,
	registro_anexo_domicilio,
	registro_anexo_domicilio_version,
	registro_anexo_edificio_compartido_niveles,
	registro_anexo_edificio_compartido_niveles_version,
	registro_anexo_estados,
	registro_anexo_informacion_edilicia,
	registro_anexo_informacion_edilicia_version,
	registro_anexo_version,
	registro_anexos_funciones,
	registro_anexos_funciones_version,
	registro_anexos_niveles,
	registro_anexos_niveles_version,
	registro_anexos_turnos,
	registro_anexos_turnos_version,
	titulos_cohortes_anexos,
	titulos_cohorte_anexo_estados,
	titulos_cohorte_anexo_seguimiento,
	titulos_egresados_anexo,
	titulos_egresados_anexo_detalle,
	titulos_matricula,
	titulos_postitulo,
	titulos_proyecto,
	registro_anexo,
--
-- Extensiones áulicas
--
	registro_extension_aulica_baja,
	registro_extension_aulica_domicilio,
	registro_extension_aulica_domicilio_version,
	registro_extension_aulica_estados,
	registro_extension_aulica_estados_version,
	registro_extension_aulica_version,
	registro_extensiones_aulicas_turnos,
	registro_extensiones_aulicas_turnos_version,
	titulos_cohortes_extensiones_aulicas,
	titulos_cohorte_extension_aulica_estados,
	registro_extension_aulica,
--
-- Establecimientos
-- 
	registro_establecimiento_autoridades,
	registro_establecimiento_autoridades_version,
	registro_establecimiento_conexion_internet,
	registro_establecimiento_conexion_internet_version,
	registro_establecimiento_domicilio,
	registro_establecimiento_domicilio_version,
	registro_establecimiento_edificio_compartido_niveles,
	registro_establecimiento_edificio_compartido_niveles_version,
	registro_establecimiento_informacion_edilicia,
	registro_establecimiento_informacion_edilicia_version,
	registro_establecimiento_version,
	registro_establecimientos_funciones,
	registro_establecimientos_funciones_version,
	registro_establecimientos_niveles,
	registro_establecimientos_niveles_version,
	registro_establecimientos_turnos,
	registro_establecimientos_turnos_version,
	registro_registro_establecimiento_version,
	registro_registro_establecimiento,
	titulos_cohortes_establecimientos,
	titulos_cohorte_establecimiento_estados,
	titulos_cohorte_establecimiento_seguimiento,
	titulos_egresados_establecimiento,
	titulos_egresados_establecimiento_detalle,
	registro_establecimiento,
--
-- Dependencias funcionales
--
	registro_dependencia_funcional,
	registro_dependencia_funcional_version
	RESTART IDENTITY
;


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('031', '', 'Eliminar datos de tablas del sistema para generar DF temporales - Ticket #157');

COMMIT;
