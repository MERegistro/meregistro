BEGIN;

CREATE TABLE "seguridad_password_remember_key" (
    "id" serial NOT NULL PRIMARY KEY,
    "usuario_id" integer NOT NULL REFERENCES "seguridad_usuario" ("id") DEFERRABLE INITIALLY DEFERRED,
    "key" varchar(255) NOT NULL
)
;


CREATE INDEX "seguridad_password_remember_key_usuario_id" ON "seguridad_password_remember_key" ("usuario_id");
CREATE INDEX idx_password_remember_key
   ON seguridad_password_remember_key USING hash ("key");

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('016', 'Seguridad', '#6');


COMMIT;
