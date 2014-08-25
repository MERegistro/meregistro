--- cohortes SD , AX y EA
SELECT j.nombre jurisdiccion, tg.nombre gestion
, e.id as clave, '1.sede' as tipo
, e.cue as cue, e.nombre as establecimiento, c.nombre as carrera, 
co.anio as cohorte, ces.anio as cursada, ce.inscriptos as inscriptos, 
ces.solo_cursan_nuevas_unidades as solo_cursan_nuevas_unidades
, ces.solo_recursan_nuevas_unidades as solo_recursan_nuevas_unidades,
ces.recursan_cursan_nuevas_unidades as recursan_cursan_nuevas_unidades
, ces.no_cursan as no_cursan, ces.egresados as egresados
---funciones en horizontal
,(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=1) as inicial
,(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=2) as continua
,(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=3) as investigacion
,(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=4) as apoyo
	---alcances en horizontal
,(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=1) as inicial
,(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=2) as primaria
,(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=3) as media
,(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=4) as superior
-- empieza query
FROM registro_jurisdiccion j
inner join titulos_carrera_jurisdiccional cj on cj.jurisdiccion_id=j.id
inner join titulos_carrera c on c.id=cj.carrera_id
inner join titulos_cohorte co on co.carrera_jurisdiccional_id=cj.id
inner join titulos_cohortes_establecimientos ce on ce.cohorte_id=co.id
inner join registro_establecimiento e on e.id=ce.establecimiento_id
inner join titulos_cohorte_establecimiento_seguimiento ces on ce.id=ces.cohorte_establecimiento_id
inner join registro_dependencia_funcional as df on df.id=e.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
--
inner join seguridad_ambito ambito on e.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where e.estado_id <> 4 --- los distintos de NO VIGENTE

union

--- anexos 
SELECT j.nombre jurisdiccion, tg.nombre gestion
, ax.establecimiento_id as clave, '2.anexo' as tipo
, ax.cue as cue, ax.nombre as establecimiento, c.nombre as carrera, 
co.anio as cohorte, caxs.anio as cursada, cax.inscriptos as inscriptos, 
caxs.solo_cursan_nuevas_unidades as solo_cursan_nuevas_unidades
, caxs.solo_recursan_nuevas_unidades as solo_recursan_nuevas_unidades
,caxs.recursan_cursan_nuevas_unidades as recursan_cursan_nuevas_unidades
, caxs.no_cursan as no_cursan, caxs.egresados as egresados
---funciones en horizontal
,(select case when axf.anexo_id is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id and f.id=1) as inicial
,(select case when axf.anexo_id  is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id  and f.id=2) as continua
,(select case when axf.anexo_id  is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id  and f.id=3) as investigacion
,(select case when axf.anexo_id  is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id  and f.id=4) as apoyo
	---alcances anexo en horizontal
,(select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa 
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=1) as inicial
,(select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=2) as primaria
,(select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=3) as media
,(select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=4) as superior
--- empieza query	
FROM registro_jurisdiccion j
inner join titulos_carrera_jurisdiccional cj on cj.jurisdiccion_id=j.id
inner join titulos_carrera c on c.id=cj.carrera_id
inner join titulos_cohorte co on co.carrera_jurisdiccional_id=cj.id
inner join titulos_cohortes_anexos cax on cax.cohorte_id=co.id
inner join registro_anexo ax on ax.id=cax.anexo_id
inner join registro_establecimiento e on e.id=ax.establecimiento_id
inner join titulos_cohorte_anexo_seguimiento caxs on cax.id=caxs.cohorte_anexo_id
inner join registro_dependencia_funcional as df on df.id=e.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
--
inner join seguridad_ambito ambito on ax.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where ax.estado_id <> 4 --- los distintos de NO VIGENTE

union 

--- las extensiones aulicas
SELECT j.nombre as jurisdiccion, tg.nombre as gestion
, ea.establecimiento_id as clave, '3.e.áulica as tipo'
, e.cue as cue, e.nombre as establecimiento, c.nombre as carrera
, co.anio as cohorte, ceas.anio as cursada, cea.inscriptos as inscriptos
, ceas.solo_cursan_nuevas_unidades as solo_cursan_nuevas_unidades
, ceas.solo_recursan_nuevas_unidades as solo_recursan_nuevas_unidades
, ceas.recursan_cursan_nuevas_unidades as recursan_cursan_nuevas_unidades
, ceas.no_cursan as no_cursan
, ceas.egresados as egresados
---funciones en horizontal
, (select case when eaf.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_funciones eaf 
	inner join registro_funcion f on f.id=eaf.funcion_id
	where eaf.extensionaulica_id=ea.id and f.id=1) as inicial
, (select case when eaf.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_funciones eaf 
	inner join registro_funcion f on f.id=eaf.funcion_id
	where eaf.extensionaulica_id=ea.id and f.id=2) as continua
, (select case when eaf.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_funciones eaf 
	inner join registro_funcion f on f.id=eaf.funcion_id
	where eaf.extensionaulica_id=ea.id and f.id=3) as investigacion
, (select case when eaf.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_funciones eaf 
	inner join registro_funcion f on f.id=eaf.funcion_id
	where eaf.extensionaulica_id=ea.id and f.id=4) as apoyo
---alcances en horizontal
, (select case when eaa.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_alcances eaa
	inner join registro_alcance al on al.id=eaa.alcance_id
	where eaa.extensionaulica_id=ea.id and al.id=1) as inicial
, (select case when eaa.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_alcances eaa
	inner join registro_alcance al on al.id=eaa.alcance_id
	where eaa.extensionaulica_id=ea.id and al.id=2) as primaria
, (select case when eaa.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_alcances eaa
	inner join registro_alcance al on al.id=eaa.alcance_id
	where eaa.extensionaulica_id=ea.id and al.id=3) as media
, (select case when eaa.extensionaulica_id is not null then 'SI' end 
	from registro_extension_aulica_alcances eaa
	inner join registro_alcance al on al.id=eaa.alcance_id
	where eaa.extensionaulica_id=ea.id and al.id=4) as superior
FROM registro_jurisdiccion j
inner join titulos_carrera_jurisdiccional cj on cj.jurisdiccion_id=j.id
inner join titulos_carrera c on c.id=cj.carrera_id
inner join titulos_cohorte co on co.carrera_jurisdiccional_id=cj.id
inner join titulos_cohortes_extensiones_aulicas cea on cea.cohorte_id=co.id

inner join registro_extension_aulica ea on ea.id=cea.extension_aulica_id
inner join registro_establecimiento e on e.id=ea.establecimiento_id
inner join titulos_cohorte_extension_aulica_seguimiento ceas on cea.id=ceas.cohorte_extension_aulica_id
inner join registro_dependencia_funcional as df on df.id=e.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
--
inner join seguridad_ambito ambito on ea.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where ea.estado_id <> 4 --- los distintos de NO VIGENTE

order by jurisdiccion, gestion, clave, tipo, cue , carrera, cohorte, cursada;
