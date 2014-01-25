--Tipo de UE: [Sede, Anexo, Extensión]
--Jurisdicción:
--Tipo de Gestión: [Estatal o Privada]
Dependencia Funcional:
--CUE:
--Nombre de la UE:
Es Unidad Académica: [Si o No]
Porcentaje de subsidio:
Año de Creación:
Origen de la norma:
Tipo de Norma:
Nro de la Norma:
---
---
Teléfono Institucional:
Interno:
Número de Fax:
Email Institucional:
Sitio Web:
---
---
Domicilio Institucional Dirección:
Domicilio Institucional Departamento:
Domicilio Institucional Localidad:
Referencia:
C.P.:
Domicilio Postal Dirección:
Domicilio Postal Departamento:
Domicilio Postal Localidad:
Referencia:
C.P.:
--
--
Apellido:
Nombre:
Fecha de Nacimiento:
Tipo de Documento:
Documento:
Teléfono:
Celular:
Email:
--
--
Uso del Edificio:
Comparte Edificio con:
Niveles:

SELECT 
	'Sede' AS "tipo_ue" 
	,jur.nombre AS "jurisdiccion"
	,tg.nombre AS "tipo_gestion"
	,df.nombre AS "dependencia_funcional"
	,CASE WHEN est.unidad_academica = True THEN 'Sí' ELSE 'No' END AS "unidad_academica"
	,tipo_subsidio.descripcion AS "porcentaje_subsidio"
	,est.anio_creacion AS "anio_creacion"
	,tipo_normativa.descripcion AS "origen_norma"
	,tipo_norma.descripcion AS "tipo_norma"
	,est.norma_creacion AS "numero_norma"
	,est.cue AS "cue", est.nombre AS "nombre_ue"
	,est.telefono AS "telefono_institucional"
	,est.interno AS "interno"
	,est.fax AS "fax"
	,est.email AS "email"
	,est.sitio_web AS "sitio_web"
	,autoridad.apellido AS "autoridad_apellido"
	,autoridad.nombre AS "autoridad_nombre"
	,autoridad.fecha_nacimiento AS "autoridad_fecha_nacimiento"
	,autoridad_tipo_doc.descripcion AS "autoridad_tipo_documento"
	,autoridad.documento AS "autoridad_documento"
	,autoridad.telefono AS "autoridad_telefono"
	,autoridad.celular AS "autoridad_celular"
	,autoridad.email AS "autoridad_email"
	,autoridad_cargo.descripcion AS "autoridad_cargo"
	,CONCAT(dom_inst.calle || ' ' || dom_inst.altura) AS "dom_inst_direccion"
	,dom_inst_departamento.nombre AS "dom_inst_departamento"
	,dom_inst_localidad.nombre AS "dom_inst_localidad"
	,dom_inst.referencia AS "dom_inst_referencia"
	,dom_inst.cp AS "dom_inst_cp"
	,CONCAT(dom_post.calle || ' ' || dom_post.altura) AS "dom_post_direccion"
	,dom_post_departamento.nombre AS "dom_post_departamento"
	,dom_post_localidad.nombre AS "dom_post_localidad"
	,dom_post.referencia AS "dom_post_referencia"
	,dom_post.cp AS "dom_post_cp"
	,tipo_dominio.descripcion AS "info_edilicia_uso_edificio"
	,tipo_compartido.descripcion AS "info_edilicia_tipo_compartido"
	,(
		SELECT array_to_string(array_agg(nivel.nombre), ', ')
		FROM registro_establecimiento_edificio_compartido_niveles info_edilicia_niveles
		INNER JOIN registro_establecimiento_informacion_edilicia info_edilicia
			ON info_edilicia_niveles.establecimientoinformacionedilicia_id = info_edilicia.id 
		INNER JOIN registro_nivel nivel ON info_edilicia_niveles.nivel_id = nivel.id
		WHERE info_edilicia.establecimiento_id = est.id
	) AS "info_edilicia_niveles"
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
LEFT JOIN registro_tipo_subsidio tipo_subsidio ON est.subsidio_id = tipo_subsidio.id
LEFT JOIN registro_tipo_normativa tipo_normativa ON est.tipo_normativa_id = tipo_normativa.id
LEFT JOIN registro_tipo_norma tipo_norma ON est.tipo_norma_id = tipo_norma.id
LEFT JOIN registro_establecimiento_domicilio dom_inst ON dom_inst.establecimiento_id = est.id AND dom_inst.tipo_domicilio_id = 1
LEFT JOIN registro_localidad dom_inst_localidad ON dom_inst.localidad_id = dom_inst_localidad.id
LEFT JOIN registro_departamento dom_inst_departamento ON dom_inst_localidad.departamento_id = dom_inst_departamento.id
LEFT JOIN registro_establecimiento_domicilio dom_post ON dom_post.establecimiento_id = est.id AND dom_post.tipo_domicilio_id = 2
LEFT JOIN registro_localidad dom_post_localidad ON dom_post.localidad_id = dom_post_localidad.id
LEFT JOIN registro_departamento dom_post_departamento ON dom_post_localidad.departamento_id = dom_post_departamento.id
LEFT JOIN registro_establecimiento_autoridades autoridad ON autoridad.establecimiento_id = est.id
LEFT JOIN seguridad_tipo_documento autoridad_tipo_doc ON autoridad.tipo_documento_id = autoridad_tipo_doc.id
LEFT JOIN registro_autoridad_cargo autoridad_cargo ON autoridad.cargo_id = autoridad_cargo.id
LEFT JOIN registro_establecimiento_informacion_edilicia info_edilicia ON info_edilicia.establecimiento_id = est.id 
LEFT JOIN registro_tipo_dominio tipo_dominio ON info_edilicia.tipo_dominio_id = tipo_dominio.id 
LEFT JOIN registro_tipo_compartido tipo_compartido ON info_edilicia.tipo_compartido_id = tipo_compartido.id 
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
