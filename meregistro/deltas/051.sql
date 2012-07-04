BEGIN;

INSERT INTO registro_tipo_conexion ("id", "nombre", "descripcion") VALUES
(1, '3G Telefonia Celular', '3G Telefonia Celular'),
(2, 'Conexión Inalambrica fija', 'Conexión Inalambrica fija'),
(3, 'Conexión por cable modem coaxil', 'Conexión por cable modem coaxil'),
(4, 'Conexión por cable modem fibra optica', 'Conexión por cable modem fibra optica'),
(5, 'Conexión satelital', 'Conexión satelital'),
(6, 'Conexión telefonica (RTC) o (Dial Up)', 'Conexión telefonica (RTC) o (Dial Up)'),
(7, 'Conexión telefonica Adsl (navega y habla al mismo tiempo)', 'Conexión telefonica Adsl (navega y habla al mismo tiempo)');

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('051', 'Registro', 'Tipos de conexión a internet');

COMMIT;
