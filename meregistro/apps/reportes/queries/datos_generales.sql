SELECT 
	'Sede' AS "tipo_ue" 
	,jur.nombre AS "jurisdiccion"
	,tg.nombre AS "tipo_gestion"
	,est.cue AS "cue", est.nombre AS "nombre_ue"
	,mat2011.profesorados AS "mat2011_profesorados"
	,mat2011.formacion_docente AS "mat2011_formacion_docente"
	,mat2011.total AS "mat2011_total"
	,mat2012.profesorados AS "mat2012_profesorados"
	,mat2012.formacion_docente AS "mat2012_formacion_docente"
	,mat2012.total AS "mat2012_total"
	,mat2013.profesorados AS "mat2013_profesorados"
	,mat2013.formacion_docente AS "mat2013_formacion_docente"
	,mat2013.total AS "mat2013_total"
	-- Mañana
	,CASE WHEN EXISTS (
		SELECT est_turno.*
		FROM registro_establecimiento_turno est_turno 
		WHERE est_turno.establecimiento_id = est.id
		AND est_turno.turno_id = 1
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_maniana"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 1
	) AS "maniana_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 1
	) AS "maniana_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_establecimiento_turno est_turno
		INNER JOIN registro_establecimiento_turno_niveles est_turno_niveles 
		ON est_turno_niveles.establecimientoturno_id = est_turno.id 
		AND est_turno.turno_id = 1
		INNER JOIN registro_nivel nivel ON est_turno_niveles.nivel_id = nivel.id
		WHERE est_turno.establecimiento_id = est.id
	) AS "maniana_niveles"
	-- Tarde
	,CASE WHEN EXISTS (
		SELECT est_turno.*
		FROM registro_establecimiento_turno est_turno 
		WHERE est_turno.establecimiento_id = est.id
		AND est_turno.turno_id = 2
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_tarde"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 2
	) AS "tarde_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 2
	) AS "tarde_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_establecimiento_turno est_turno
		INNER JOIN registro_establecimiento_turno_niveles est_turno_niveles 
		ON est_turno_niveles.establecimientoturno_id = est_turno.id 
		AND est_turno.turno_id = 2
		INNER JOIN registro_nivel nivel ON est_turno_niveles.nivel_id = nivel.id
		WHERE est_turno.establecimiento_id = est.id
	) AS "tarde_niveles"
	-- Noche
	,CASE WHEN EXISTS (
		SELECT est_turno.*
		FROM registro_establecimiento_turno est_turno 
		WHERE est_turno.establecimiento_id = est.id
		AND est_turno.turno_id = 3
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_noche"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 3
	) AS "noche_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_establecimiento_turno 
		ON registro_establecimiento_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_establecimiento_turno.establecimiento_id = est.id
		AND registro_establecimiento_turno.turno_id = 3
	) AS "noche_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_establecimiento_turno est_turno
		INNER JOIN registro_establecimiento_turno_niveles est_turno_niveles 
		ON est_turno_niveles.establecimientoturno_id = est_turno.id 
		AND est_turno.turno_id = 3
		INNER JOIN registro_nivel nivel ON est_turno_niveles.nivel_id = nivel.id
		WHERE est_turno.establecimiento_id = est.id
	) AS "noche_niveles"
FROM registro_establecimiento est
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_jurisdiccion jur ON df.jurisdiccion_id = jur.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
LEFT JOIN registro_establecimiento_matricula mat2011 on mat2011.establecimiento_id = est.id AND mat2011.anio = 2011
LEFT JOIN registro_establecimiento_matricula mat2012 on mat2012.establecimiento_id = est.id AND mat2012.anio = 2012
LEFT JOIN registro_establecimiento_matricula mat2013 on mat2013.establecimiento_id = est.id AND mat2013.anio = 2013

UNION 

SELECT 
	'Anexo' AS "tipo_ue" 
	,jur.nombre AS "jurisdiccion"
	,tg.nombre AS "tipo_gestion"
	,anexo.cue AS "cue", anexo.nombre AS "nombre_ue"
	,mat2011.profesorados AS "mat2011_profesorados"
	,mat2011.formacion_docente AS "mat2011_formacion_docente"
	,mat2011.total AS "mat2011_total"
	,mat2012.profesorados AS "mat2012_profesorados"
	,mat2012.formacion_docente AS "mat2012_formacion_docente"
	,mat2012.total AS "mat2012_total"
	,mat2013.profesorados AS "mat2013_profesorados"
	,mat2013.formacion_docente AS "mat2013_formacion_docente"
	,mat2013.total AS "mat2013_total"
	-- Mañana
	,CASE WHEN EXISTS (
		SELECT anexo_turno.*
		FROM registro_anexo_turno anexo_turno 
		WHERE anexo_turno.anexo_id = anexo.id
		AND anexo_turno.turno_id = 1
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_maniana"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 1
	) AS "maniana_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 1
	) AS "maniana_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_anexo_turno anexo_turno
		INNER JOIN registro_anexo_turno_niveles anexo_turno_niveles 
		ON anexo_turno_niveles.anexoturno_id = anexo_turno.id 
		AND anexo_turno.turno_id = 1
		INNER JOIN registro_nivel nivel ON anexo_turno_niveles.nivel_id = nivel.id
		WHERE anexo_turno.anexo_id = anexo.id
	) AS "maniana_niveles"
	-- Tarde
	,CASE WHEN EXISTS (
		SELECT anexo_turno.*
		FROM registro_anexo_turno anexo_turno 
		WHERE anexo_turno.anexo_id = anexo.id
		AND anexo_turno.turno_id = 2
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_tarde"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 2
	) AS "tarde_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 2
	) AS "tarde_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_anexo_turno anexo_turno
		INNER JOIN registro_anexo_turno_niveles anexo_turno_niveles 
		ON anexo_turno_niveles.anexoturno_id = anexo_turno.id 
		AND anexo_turno.turno_id = 2
		INNER JOIN registro_nivel nivel ON anexo_turno_niveles.nivel_id = nivel.id
		WHERE anexo_turno.anexo_id = anexo.id
	) AS "tarde_niveles"
	-- Noche
	,CASE WHEN EXISTS (
		SELECT anexo_turno.*
		FROM registro_anexo_turno anexo_turno 
		WHERE anexo_turno.anexo_id = anexo.id
		AND anexo_turno.turno_id = 3
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_noche"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 3
	) AS "noche_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_anexo_turno 
		ON registro_anexo_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_anexo_turno.anexo_id = anexo.id
		AND registro_anexo_turno.turno_id = 3
	) AS "noche_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_anexo_turno anexo_turno
		INNER JOIN registro_anexo_turno_niveles anexo_turno_niveles 
		ON anexo_turno_niveles.anexoturno_id = anexo_turno.id 
		AND anexo_turno.turno_id = 3
		INNER JOIN registro_nivel nivel ON anexo_turno_niveles.nivel_id = nivel.id
		WHERE anexo_turno.anexo_id = anexo.id
	) AS "noche_niveles"
FROM registro_anexo anexo
INNER JOIN registro_establecimiento est ON anexo.establecimiento_id = est.id
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_jurisdiccion jur ON df.jurisdiccion_id = jur.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
LEFT JOIN registro_anexo_matricula mat2011 on mat2011.anexo_id = anexo.id AND mat2011.anio = 2011
LEFT JOIN registro_anexo_matricula mat2012 on mat2012.anexo_id = anexo.id AND mat2012.anio = 2012
LEFT JOIN registro_anexo_matricula mat2013 on mat2013.anexo_id = anexo.id AND mat2013.anio = 2013

UNION 

SELECT 
	'Extensión Áulica' AS "tipo_ue" 
	,jur.nombre AS "jurisdiccion"
	,tg.nombre AS "tipo_gestion"
	,extension_aulica.cue AS "cue", extension_aulica.nombre AS "nombre_ue"
	,mat2011.profesorados AS "mat2011_profesorados"
	,mat2011.formacion_docente AS "mat2011_formacion_docente"
	,mat2011.total AS "mat2011_total"
	,mat2012.profesorados AS "mat2012_profesorados"
	,mat2012.formacion_docente AS "mat2012_formacion_docente"
	,mat2012.total AS "mat2012_total"
	,mat2013.profesorados AS "mat2013_profesorados"
	,mat2013.formacion_docente AS "mat2013_formacion_docente"
	,mat2013.total AS "mat2013_total"
	-- Mañana
	,CASE WHEN EXISTS (
		SELECT extension_aulica_turno.*
		FROM registro_extension_aulica_turno extension_aulica_turno 
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND extension_aulica_turno.turno_id = 1
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_maniana"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 1
	) AS "maniana_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 1
	) AS "maniana_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_extension_aulica_turno extension_aulica_turno
		INNER JOIN registro_extension_aulica_turno_niveles extension_aulica_turno_niveles 
		ON extension_aulica_turno_niveles.extensionaulicaturno_id = extension_aulica_turno.id 
		AND extension_aulica_turno.turno_id = 1
		INNER JOIN registro_nivel nivel ON extension_aulica_turno_niveles.nivel_id = nivel.id
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
	) AS "maniana_niveles"
	-- Tarde
	,CASE WHEN EXISTS (
		SELECT extension_aulica_turno.*
		FROM registro_extension_aulica_turno extension_aulica_turno 
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND extension_aulica_turno.turno_id = 2
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_tarde"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 2
	) AS "tarde_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 2
	) AS "tarde_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_extension_aulica_turno extension_aulica_turno
		INNER JOIN registro_extension_aulica_turno_niveles extension_aulica_turno_niveles 
		ON extension_aulica_turno_niveles.extensionaulicaturno_id = extension_aulica_turno.id 
		AND extension_aulica_turno.turno_id = 2
		INNER JOIN registro_nivel nivel ON extension_aulica_turno_niveles.nivel_id = nivel.id
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
	) AS "tarde_niveles"
	-- Noche
	,CASE WHEN EXISTS (
		SELECT extension_aulica_turno.*
		FROM registro_extension_aulica_turno extension_aulica_turno 
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND extension_aulica_turno.turno_id = 3
	) THEN 'Posee' ELSE 'No Posee' END AS "turno_noche"
	,(
		SELECT tipo_dominio.descripcion 
		FROM registro_tipo_dominio tipo_dominio 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_dominio_id = tipo_dominio.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 3
	) AS "noche_uso_edificio"
	,(
		SELECT tipo_compartido.descripcion 
		FROM registro_tipo_compartido tipo_compartido 
		INNER JOIN registro_extension_aulica_turno 
		ON registro_extension_aulica_turno.tipo_compartido_id = tipo_compartido.id
		AND registro_extension_aulica_turno.extension_aulica_id = extension_aulica.id
		AND registro_extension_aulica_turno.turno_id = 3
	) AS "noche_comparte_con"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_extension_aulica_turno extension_aulica_turno
		INNER JOIN registro_extension_aulica_turno_niveles extension_aulica_turno_niveles 
		ON extension_aulica_turno_niveles.extensionaulicaturno_id = extension_aulica_turno.id 
		AND extension_aulica_turno.turno_id = 3
		INNER JOIN registro_nivel nivel ON extension_aulica_turno_niveles.nivel_id = nivel.id
		WHERE extension_aulica_turno.extension_aulica_id = extension_aulica.id
	) AS "noche_niveles"
FROM registro_extension_aulica extension_aulica
INNER JOIN registro_establecimiento est ON extension_aulica.establecimiento_id = est.id
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_jurisdiccion jur ON df.jurisdiccion_id = jur.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
LEFT JOIN registro_extension_aulica_matricula mat2011 on mat2011.extension_aulica_id = extension_aulica.id AND mat2011.anio = 2011
LEFT JOIN registro_extension_aulica_matricula mat2012 on mat2012.extension_aulica_id = extension_aulica.id AND mat2012.anio = 2012
LEFT JOIN registro_extension_aulica_matricula mat2013 on mat2013.extension_aulica_id = extension_aulica.id AND mat2013.anio = 2013

ORDER BY "cue"
;
