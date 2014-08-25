-- matricula
select  j.nombre as jurisdiccion, tg.nombre as gestion, e.id  clave, '1.sede' as tipo, e.cue , e.nombre,
m.anio as anio, m.profesorados, m.postitulos, m.formacion_continua, m.formacion_docente, m.tecnicaturas, m.total,
---funciones en horizontal
(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=1) as inicial,
(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=2) as continua,
(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=3) as investigacion,
(select case when ef.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_funciones ef 
	inner join registro_funcion f on f.id=ef.funcion_id
	where ef.establecimiento_id=e.id and f.id=4) as apoyo,
	---alcances en horizontal
(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=1) as inicial,
(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=2) as primaria,
(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=3) as media,
(select case when ea.establecimiento_id is not null then 'SI' end 
	from registro_establecimientos_alcances ea 
	inner join registro_alcance al on al.id=ea.alcance_id
	where ea.establecimiento_id=e.id and al.id=4) as superior
---empieza el query
from registro_establecimiento as e
inner join registro_dependencia_funcional as df on df.id=e.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
inner join registro_jurisdiccion j on j.id=df.jurisdiccion_id
left join registro_establecimiento_matricula m on m.establecimiento_id=e.id
--
inner join seguridad_ambito ambito on e.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where e.estado_id<>4 ---son los distintos de NO VIGENTE

union 

---union de anexos
select  j.nombre as jurisdiccion, tg.nombre as gestion, ax.establecimiento_id as clave, '2.anexo' as tipo
, ax.cue as cue, ax.nombre 
, max.anio as anio, max.profesorados, max.postitulos, max.formacion_continua, max.formacion_docente, max.tecnicaturas, max.total
---funciones en horizontal
, (select case when axf.anexo_id is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id and f.id=1) as inicial
, (select case when axf.anexo_id is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id and f.id=2) as continua
, (select case when axf.anexo_id is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id and f.id=3) as investigacion
, (select case when axf.anexo_id is not null then 'SI' end 
	from registro_anexos_funciones axf 
	inner join registro_funcion f on f.id=axf.funcion_id
	where axf.anexo_id=ax.id and f.id=4) as apoyo
---alcances en horizontal
, (select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=1) as inicial
, (select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa 
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=2) as primaria
, (select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=3) as media
, (select case when axa.anexo_id is not null then 'SI' end 
	from registro_anexos_alcances axa 
	inner join registro_alcance al on al.id=axa.alcance_id
	where axa.anexo_id=ax.id and al.id=4) as superior
---empieza el query
from registro_anexo as ax
inner join registro_establecimiento e2 on ax.establecimiento_id=e2.id
inner join registro_dependencia_funcional as df on df.id=e2.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
inner join registro_jurisdiccion j on j.id=df.jurisdiccion_id
left join registro_anexo_matricula max on max.anexo_id=ax.id
--
inner join seguridad_ambito ambito on ax.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where ax.estado_id<>4 ---son los distintos de NO VIGENTE

union

---union de extensiones aulicas
select j.nombre as jurisdiccion, tg.nombre as gestion, ea.establecimiento_id as clave, '3.e.áulica as tipo'
, ea.cue as cue, ea.nombre
, mea.anio as anio, mea.profesorados, mea.postitulos, mea.formacion_continua, mea.formacion_docente, mea.tecnicaturas, mea.total
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
from registro_extension_aulica as ea
inner join registro_establecimiento e3 on ea.establecimiento_id=e3.id
inner join registro_dependencia_funcional as df on df.id=e3.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
inner join registro_jurisdiccion j on j.id=df.jurisdiccion_id
left join registro_extension_aulica_matricula mea on mea.extension_aulica_id=ea.id
--
inner join seguridad_ambito ambito on ea.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--
where ea.estado_id<>4 ---son los distintos de NO VIGENTE

order by jurisdiccion, gestion, clave, tipo, anio,  cue;

--- nota: debería verificarse si las ea y las sd tienen cantidades??
