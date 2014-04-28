select
    esax.nombre, j.nombre as jurisdiccion, tg.nombre as gestion, ax.cue, ax.nombre as anexo, ax.telefono, ax.email, df.nombre as dep_funcional,
    ---son los turno en horizontal
    (select case when et.turno_id is not null then 'TM' end from registro_anexo_turno et where et.anexo_id=ax.id and et.turno_id=1) as tm,
    (select case when et.turno_id is not null then 'TT' end from registro_anexo_turno et where et.anexo_id=ax.id and et.turno_id=2) as tt,
    (select case when et.turno_id is not null then 'TN' end from registro_anexo_turno et where et.anexo_id=ax.id and et.turno_id=3) as tn,

    insti.calle as calle_institucional, insti.altura as altura_institucional, insti.referencia as referencia_institucional, insti.cp as cp_institucional, insti.localidad as localidad_institucional,
    post.calle as calle_postal, post.altura as altura_postal, post.referencia as referencia_postal, post.cp as cp_postal, post.localidad as localidad_postal,
    ---conexion si no
    case when ci.tiene is not null then 'SI' end as conexion,
    ---compartido si no
    case when comp.comparte is not null then 'SI' end as compartido,

    ---funciones en horizontal
    (select case when ef.anexo_id is not null then 'SI' end 
        from registro_anexos_funciones ef 
        inner join registro_funcion f on f.id=ef.funcion_id
        where ef.anexo_id=ax.id and f.id=1) as inicial_funcion,
    (select case when ef.anexo_id is not null then 'SI' end 
        from registro_anexos_funciones  ef 
        inner join registro_funcion f on f.id=ef.funcion_id
        where ef.anexo_id=ax.id and f.id=2) as continua,
    (select case when ef.anexo_id is not null then 'SI' end 
        from registro_anexos_funciones  ef 
        inner join registro_funcion f on f.id=ef.funcion_id
        where ef.anexo_id=ax.id and f.id=3) as investigacion,
    (select case when ef.anexo_id is not null then 'SI' end 
        from registro_anexos_funciones  ef 
        inner join registro_funcion f on f.id=ef.funcion_id
        where ef.anexo_id=ax.id and f.id=4) as apoyo,
    ---alcances en horizontal
    (select case when ea.anexo_id is not null then 'SI' end 
        from registro_anexos_alcances ea 
        inner join registro_alcance al on al.id=ea.alcance_id
        where ea.anexo_id=ax.id and al.id=1) as inicial,
    (select case when ea.anexo_id is not null then 'SI' end 
        from registro_anexos_alcances ea 
        inner join registro_alcance al on al.id=ea.alcance_id
        where ea.anexo_id=ax.id and al.id=2) as primaria,
    (select case when ea.anexo_id is not null then 'SI' end 
        from registro_anexos_alcances ea 
        inner join registro_alcance al on al.id=ea.alcance_id
        where ea.anexo_id=ax.id and al.id=3) as media,
    (select case when ea.anexo_id is not null then 'SI' end 
        from registro_anexos_alcances ea 
        inner join registro_alcance al on al.id=ea.alcance_id
        where ea.anexo_id=ax.id and al.id=4) as superior
----empieza el query normal		
from public.registro_anexo as ax
inner join registro_estado_anexo esax on esax.id=ax.estado_id
inner join registro_establecimiento e on ax.establecimiento_id=e.id
inner join registro_dependencia_funcional as df on df.id=e.dependencia_funcional_id
inner join registro_tipo_gestion tg on tg.id=df.tipo_gestion_id
inner join registro_jurisdiccion j on j.id=df.jurisdiccion_id
--
inner join seguridad_ambito ambito on ax.ambito_id = ambito.id and ambito.path ilike {{AMBITO_PATH}}
--


---son los domicilios institucionales
left join 
	(
	---al primer domicilio del anexo le agrega los datos de calle
	---estas son las direcciones institucionales pero tomando sòlo la primera de cada anexo
	select domi.calle, domi.altura, domi.referencia, domi.cp, l.nombre as localidad, domi.id, domi.anexo_id
	from registro_anexo_domicilio domi
	inner join registro_localidad l on l.id=domi.localidad_id
	inner join 
		(
		---toma el primer domicilio de cada establecimeinto
		select min(d1.id) as d_ins_id, d1.anexo_id
		from registro_anexo_domicilio as d1 
		where d1.tipo_domicilio_id=1 
		group by d1.anexo_id

		) as di on di.d_ins_id=domi.id 
	) as insti on insti.anexo_id = ax.id

left join 
---son los domicilios postales
	(
	---al primer domicilio del establecimieto le agrega los datos de calle
	---estas son las direcciones institucionales pero tomando sòlo la primera de cada establecimiento
	select domp.calle, domp.altura, domp.referencia, domp.cp, l.nombre as localidad, domp.id, domp.anexo_id
	from registro_anexo_domicilio domp
	inner join registro_localidad l on l.id=domp.localidad_id
	inner join 
		(
		---toma el primer domicilio de cada establecimeinto
		select min(d2.id) as d_ins_id, d2.anexo_id
		from registro_anexo_domicilio as d2 
		where d2.tipo_domicilio_id=2
		group by d2.anexo_id
		
		) as dp on dp.d_ins_id=domp.id 
	) as post on post.anexo_id = ax.id
left join 
---son las conexiones a internet
	(
	---conexion a internet tiene que ser solo un registro por establecimiento
	select ax_axci.id as tiene
	from registro_anexo ax_axci
	inner join registro_anexo_conexion_internet eci on eci.anexo_id=ax_axci.id
	group by ax_axci.id order by ax_axci.id
	) as ci on ci.tiene=e.id
left join 
---son los establecimientos que comparten edificio
	(
	select ie.anexo_id as comparte
	from registro_anexo_informacion_edilicia ie 
	where ie.tipo_compartido_id is not null
	group by ie.anexo_id
	) as comp on comp.comparte=ax.id
where esax.id <> 4 --- no vigente	
order by jurisdiccion, gestion, ax.cue;
---nota: el alcance y la funcion no son de una carrera en particular sino del anexo en general
---al filtrar por carrera, el alcance o la funcion podrían no ser la que le correspondan a la carrera sino
---al conjunto de las carreras del establecimiento
---se muestran los anexos cuyo estado no es 'no vigente'
