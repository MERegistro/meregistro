BEGIN;

UPDATE titulos_cohortes_anexos tc_ue
SET cohorte_id = 
(SELECT MIN(c.id) FROM titulos_cohorte c 
 INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
   WHERE
   c.anio = (SELECT anio FROM titulos_cohorte c2 WHERE c2.id = tc_ue.cohorte_id)
   AND cj.carrera_id = (SELECT cj2.carrera_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
		WHERE c2.id = tc_ue.cohorte_id
		)
   AND cj.jurisdiccion_id = (SELECT cj2.jurisdiccion_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
        WHERE c2.id = tc_ue.cohorte_id
		)
);

UPDATE titulos_cohortes_establecimientos tc_ue
SET cohorte_id = 
(SELECT MIN(c.id) FROM titulos_cohorte c 
 INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
   WHERE
   c.anio = (SELECT anio FROM titulos_cohorte c2 WHERE c2.id = tc_ue.cohorte_id)
   AND cj.carrera_id = (SELECT cj2.carrera_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
		WHERE c2.id = tc_ue.cohorte_id
		)
   AND cj.jurisdiccion_id = (SELECT cj2.jurisdiccion_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
        WHERE c2.id = tc_ue.cohorte_id
		)
);

UPDATE titulos_cohortes_extensiones_aulicas tc_ue
SET cohorte_id = 
(SELECT MIN(c.id) FROM titulos_cohorte c 
 INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
   WHERE
   c.anio = (SELECT anio FROM titulos_cohorte c2 WHERE c2.id = tc_ue.cohorte_id)
   AND cj.carrera_id = (SELECT cj2.carrera_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
		WHERE c2.id = tc_ue.cohorte_id
		)
   AND cj.jurisdiccion_id = (SELECT cj2.jurisdiccion_id FROM titulos_cohorte c2
		INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id
        WHERE c2.id = tc_ue.cohorte_id
		)
);

UPDATE titulos_carrera_jurisdiccional_cohorte c
SET carrera_jurisdiccional_id = 
(SELECT MIN(cj.id) FROM titulos_carrera_jurisdiccional cj 
   WHERE
   cj.carrera_id = (SELECT cj2.carrera_id FROM titulos_carrera_jurisdiccional cj2
		WHERE cj2.id = c.carrera_jurisdiccional_id
		)
   AND cj.jurisdiccion_id = (SELECT cj2.jurisdiccion_id FROM titulos_carrera_jurisdiccional cj2
		WHERE cj2.id = c.carrera_jurisdiccional_id
		)
);

DELETE FROM titulos_cohorte c1 WHERE EXISTS
 (SELECT 1 FROM titulos_cohorte c2 
   INNER JOIN titulos_carrera_jurisdiccional cj2 ON c2.carrera_jurisdiccional_id = cj2.id WHERE
    c2.id < c1.id
    AND c2.anio = c1.anio
    AND cj2.carrera_id = (SELECT carrera_id FROM titulos_carrera_jurisdiccional WHERE id = c1.carrera_jurisdiccional_id)
    AND cj2.jurisdiccion_id = (SELECT jurisdiccion_id FROM titulos_carrera_jurisdiccional WHERE id = c1.carrera_jurisdiccional_id)
  );

DELETE FROM titulos_carrera_jurisdiccional_estados t WHERE EXISTS
  (SELECT 1 FROM titulos_carrera_jurisdiccional cj2
    WHERE 
	cj2.id < t.carrera_jurisdiccional_id
	AND cj2.carrera_id = (SELECT carrera_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrera_jurisdiccional_id)
	AND cj2.jurisdiccion_id = (SELECT jurisdiccion_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrera_jurisdiccional_id)
  );

DELETE FROM titulos_carreras_jurisdiccionales_normativas t WHERE EXISTS
  (SELECT 1 FROM titulos_carrera_jurisdiccional cj2
    WHERE 
	cj2.id < t.carrerajurisdiccional_id
	AND cj2.carrera_id = (SELECT carrera_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrerajurisdiccional_id)
	AND cj2.jurisdiccion_id = (SELECT jurisdiccion_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrerajurisdiccional_id)
  );

UPDATE titulos_cohorte t SET carrera_jurisdiccional_id = 
  (SELECT MIN(cj2.id) FROM titulos_carrera_jurisdiccional cj2
    WHERE 
	 cj2.carrera_id = (SELECT carrera_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrera_jurisdiccional_id)
	AND cj2.jurisdiccion_id = (SELECT jurisdiccion_id FROM titulos_carrera_jurisdiccional WHERE id = t.carrera_jurisdiccional_id)
  );

DELETE FROM titulos_carrera_jurisdiccional cj1 WHERE EXISTS
  (SELECT 1 FROM titulos_carrera_jurisdiccional cj2
    WHERE 
	cj2.id < cj1.id
	AND cj2.carrera_id = cj1.carrera_id
	AND cj2.jurisdiccion_id = cj1.jurisdiccion_id
  );


DELETE FROM titulos_carrera_jurisdiccional_cohorte t1
WHERE EXISTS
  (SELECT 1 FROM titulos_carrera_jurisdiccional_cohorte t2
    WHERE t2.id < t1.id AND t2.carrera_jurisdiccional_id = t1.carrera_jurisdiccional_id
       AND t2.primera_cohorte_autorizada = t1.primera_cohorte_autorizada
       AND t2.ultima_cohorte_autorizada = t1.ultima_cohorte_autorizada);

UPDATE titulos_cohorte_anexo_estados SET estado_id = 3;

UPDATE titulos_cohorte_establecimiento_estados SET estado_id = 3;

UPDATE titulos_cohorte_extension_aulica_estados SET estado_id = 3;

COMMIT;
