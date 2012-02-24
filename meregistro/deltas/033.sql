BEGIN;



CREATE TABLE "seguridad_credencial_credenciales_hijas" (
    "id" serial NOT NULL PRIMARY KEY,
    "from_credencial_id" integer NOT NULL,
    "to_credencial_id" integer NOT NULL,
    UNIQUE ("from_credencial_id", "to_credencial_id")
)
;

ALTER TABLE "seguridad_credencial_credenciales_hijas" ADD CONSTRAINT "from_credencial_id_refs_id_3045f4d9" FOREIGN KEY ("from_credencial_id") REFERENCES "seguridad_credencial" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "seguridad_credencial_credenciales_hijas" ADD CONSTRAINT "to_credencial_id_refs_id_3045f4d9" FOREIGN KEY ("to_credencial_id") REFERENCES "seguridad_credencial" ("id") DEFERRABLE INITIALLY DEFERRED;

INSERT INTO seguridad_credencial_credenciales_hijas (from_credencial_id, to_credencial_id)
VALUES 
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_modificar')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_alta'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_baja')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_modificar'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_consulta')
),
(
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_baja'),
(SELECT id FROM seguridad_credencial WHERE nombre = 'reg_df_modificar')
);

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('033', 'Seguridad', 'Ticket #160');

COMMIT;

