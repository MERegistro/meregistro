BEGIN;

DELETE FROM titulos_cohorte_establecimiento_seguimiento
WHERE cohorte_establecimiento_id = 13846;

DELETE FROM titulos_cohorte_establecimiento_estados
WHERE cohorte_establecimiento_id IN(
    19150, 
    17703, 
    14131, 
    17509, 
    19151, 
    13926, 
    14458, 
    14460, 
    14125, 
    14129, 
    13847,
    13846,
    19321, 
    19313, 
    19316, 
    19318
);

DELETE FROM titulos_cohortes_establecimientos
WHERE id IN(
    19150, 
    17703, 
    14131, 
    17509, 
    19151, 
    13926, 
    14458, 
    14460, 
    14125, 
    14129, 
    13847,
    13846,
    19321, 
    19313, 
    19316, 
    19318
);


INSERT INTO deltas_sql (numero, app, comentario) VALUES ('133', 'Cohortes', 'Eliminación cohortes de establecimiento repetidas');

COMMIT;
