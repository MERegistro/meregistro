
#
# Genera los SQL necesarios para auditar ciertas tablas.
#


# Lista de tablas a auditar, la definicion de las tablas debe venir en el
# archivo de entrada input.sql
#
tablas_auditar = [
'seguridad_usuario',
'seguridad_perfil',
'seguridad_bloqueo_log',
'registro_anexo',
'registro_anexo_conexion_internet',
'registro_anexo_domicilio',
'registro_anexo_edificio_compartido_niveles',
'registro_anexo_informacion_edilicia',
'registro_anexos_funciones',
'registro_anexos_niveles',
'registro_anexos_turnos',
'registro_autoridad_cargo',
'registro_dependencia_funcional',
'registro_establecimiento',
'registro_establecimiento_autoridades',
'registro_establecimiento_conexion_internet',
'registro_establecimiento_domicilio',
'registro_establecimiento_edificio_compartido_niveles',
'registro_establecimiento_informacion_edilicia',
'registro_establecimientos_funciones',
'registro_establecimientos_niveles',
'registro_establecimientos_turnos',
'registro_estado_anexo',
'registro_estado_establecimiento',
'registro_estado_extension_aulica',
'registro_extension_aulica',
'registro_extension_aulica_domicilio',
'registro_extension_aulica_estados',
'registro_extensiones_aulicas_turnos',
'registro_registro_establecimiento'
]
def auditar(definition):
    lines = definition.split("\n")
    table = lines[0].split(' ')[2]
    if table not in tablas_auditar:
        return
    fields_def = map(lambda s: s.replace(',', '').strip(),
        filter(lambda s: "CREATE" not in s and"CONSTRAINT" not in s and "REFERENCES" not in s and "ACTION" not in s and s.strip() != '(' and s.strip() != ')' and s.strip() != '' and s.strip() != ');',
               lines)
        )
    fields = map(lambda s: s.split(" ")[0], fields_def)
    #print """ALTER TABLE """+table+""" ADD COLUMN last_user_id integer;"""
    #return
    print """
DROP TABLE IF EXISTS """+table+"""_version;
CREATE TABLE """+table+"""_version
(
"""
    for f in fields_def:
        print " ", f, ","
    print """
  last_user_id integer,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  "version" bigint NOT NULL,
  deleted boolean,
  CONSTRAINT """+table+"""_version_pkey PRIMARY KEY (id, "version")
)
WITH (
  OIDS=FALSE
);


CREATE OR REPLACE FUNCTION auditar_"""+table+"""()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM """+table+"""_version
WHERE id = NEW.id;

IF (vers = 1) THEN
  NEW.created_at = NOW();
  NEW.updated_at = NOW();
END IF;

INSERT INTO """+table+"""_version(
"""
    for f in fields:
        print " ", f, ","
    print """
  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (
"""
    for f in fields:
        print "NEW.%s," % f
    print """

  NEW.last_user_id,
  CASE WHEN vers > 1 THEN NEW.created_at ELSE NOW() END,
  NOW(),
  vers,
  FALSE
);

RETURN NEW;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar ON """+table+""";

CREATE TRIGGER auditar
BEFORE INSERT OR UPDATE
ON """+table+"""
FOR EACH ROW
EXECUTE PROCEDURE auditar_"""+table+"""();


CREATE OR REPLACE FUNCTION auditar_"""+table+"""_del()
RETURNS "trigger" AS $$
DECLARE
    vers int;
BEGIN

SELECT INTO vers COALESCE(MAX("version"),0 )+1
FROM """+table+"""_version
WHERE id = OLD.id;

INSERT INTO """+table+"""_version(
"""
    for f in fields:
        print " ", f, ","
    print """
  last_user_id,
  created_at,
  updated_at,
  "version",
  deleted
)
VALUES (
"""
    for f in fields:
        print "OLD.%s," % f
    print """

  OLD.last_user_id,
  CASE WHEN vers > 1 THEN OLD.created_at ELSE NOW() END,
  NOW(),
  vers,
  TRUE
);

RETURN OLD;
END;

$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS auditar_del ON """+table+""";

CREATE TRIGGER auditar_del
BEFORE DELETE
ON """+table+"""
FOR EACH ROW
EXECUTE PROCEDURE auditar_"""+table+"""_del();
"""


#TODO: implementar generacion de los SP auditar y auditar_del

fp = open('input.sql', 'r')

table_def = ''
for l in fp.readlines():
    if "CREATE TABLE" in l:
        table_def = l
    elif ");" in l and table_def != '':
        table_def += l
        auditar(table_def)
        table_def = ''
    elif table_def != '':
        table_def += l

fp.close()

