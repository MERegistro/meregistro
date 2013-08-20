UPDATE validez_nacional_validez_nacional vn SET
	carrera = c.nombre, titulo_nacional = tn.nombre, 
	primera_cohorte = s.primera_cohorte, ultima_cohorte = s.ultima_cohorte, 
	dictamen_cofev = s.dictamen_cofev, normativas_nacionales = s.normativas_nacionales, 
	normativa_jurisdiccional = s.normativa_jurisdiccional_migrada
FROM validez_nacional_solicitud s
INNER JOIN titulos_carrera c ON s.carrera_id = c.id
INNER JOIN titulos_titulo_nacional tn ON s.titulo_nacional_id = tn.id
WHERE vn.solicitud_id = s.id
;
