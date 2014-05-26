BEGIN;

--
INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES ('Postítulos', 'Postítulos', '/postitulos/');




--
-- TOC entry 487 (class 1259 OID 22383)
-- Dependencies: 6
-- Name: postitulos_carrera_postitulo_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carrera_postitulo_estados (
    id integer NOT NULL,
    carrera_postitulo_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 486 (class 1259 OID 22381)
-- Dependencies: 487 6
-- Name: postitulos_carrera_postitulo_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2935 (class 0 OID 0)
-- Dependencies: 486
-- Name: postitulos_carrera_postitulo_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_estados_id_seq OWNED BY postitulos_carrera_postitulo_estados.id;


--
-- TOC entry 511 (class 1259 OID 22570)
-- Dependencies: 6
-- Name: postitulos_carrera_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carrera_postitulo_jurisdiccional (
    id integer NOT NULL,
    carrera_postitulo_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL,
    estado_id integer NOT NULL,
    revisado_jurisdiccion boolean
);


--
-- TOC entry 513 (class 1259 OID 22600)
-- Dependencies: 6
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carrera_postitulo_jurisdiccional_estados (
    id integer NOT NULL,
    carrera_postitulo_jurisdiccional_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 512 (class 1259 OID 22598)
-- Dependencies: 513 6
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_jurisdiccional_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2936 (class 0 OID 0)
-- Dependencies: 512
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_jurisdiccional_estados_id_seq OWNED BY postitulos_carrera_postitulo_jurisdiccional_estados.id;


--
-- TOC entry 510 (class 1259 OID 22568)
-- Dependencies: 6 511
-- Name: postitulos_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2937 (class 0 OID 0)
-- Dependencies: 510
-- Name: postitulos_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_jurisdiccional_id_seq OWNED BY postitulos_carrera_postitulo_jurisdiccional.id;


--
-- TOC entry 485 (class 1259 OID 22362)
-- Dependencies: 6
-- Name: postitulos_carrerapostitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carrerapostitulo (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    estado_id integer NOT NULL,
    observaciones character varying(255),
    fecha_alta date NOT NULL,
    carrera_sin_orientacion boolean NOT NULL
);


--
-- TOC entry 484 (class 1259 OID 22360)
-- Dependencies: 6 485
-- Name: postitulos_carrerapostitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrerapostitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2938 (class 0 OID 0)
-- Dependencies: 484
-- Name: postitulos_carrerapostitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrerapostitulo_id_seq OWNED BY postitulos_carrerapostitulo.id;


--
-- TOC entry 483 (class 1259 OID 22347)
-- Dependencies: 6
-- Name: postitulos_carreras_postitulo_jurisdicciones; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carreras_postitulo_jurisdicciones (
    id integer NOT NULL,
    carrerapostitulo_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL
);


--
-- TOC entry 482 (class 1259 OID 22345)
-- Dependencies: 483 6
-- Name: postitulos_carreras_postitulo_jurisdicciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carreras_postitulo_jurisdicciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2939 (class 0 OID 0)
-- Dependencies: 482
-- Name: postitulos_carreras_postitulo_jurisdicciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carreras_postitulo_jurisdicciones_id_seq OWNED BY postitulos_carreras_postitulo_jurisdicciones.id;


--
-- TOC entry 509 (class 1259 OID 22555)
-- Dependencies: 6
-- Name: postitulos_carreras_postitulos_normativas; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carreras_postitulos_normativas (
    id integer NOT NULL,
    carrerapostitulojurisdiccional_id integer NOT NULL,
    normativapostitulo_id integer NOT NULL
);


--
-- TOC entry 508 (class 1259 OID 22553)
-- Dependencies: 509 6
-- Name: postitulos_carreras_postitulos_normativas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carreras_postitulos_normativas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2940 (class 0 OID 0)
-- Dependencies: 508
-- Name: postitulos_carreras_postitulos_normativas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carreras_postitulos_normativas_id_seq OWNED BY postitulos_carreras_postitulos_normativas.id;


--
-- TOC entry 481 (class 1259 OID 22337)
-- Dependencies: 6
-- Name: postitulos_estado_carrera_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_carrera_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 480 (class 1259 OID 22335)
-- Dependencies: 481 6
-- Name: postitulos_estado_carrera_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_carrera_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2941 (class 0 OID 0)
-- Dependencies: 480
-- Name: postitulos_estado_carrera_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_carrera_postitulo_id_seq OWNED BY postitulos_estado_carrera_postitulo.id;


--
-- TOC entry 503 (class 1259 OID 22517)
-- Dependencies: 6
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_carrera_postitulo_jurisdiccional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 502 (class 1259 OID 22515)
-- Dependencies: 6 503
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_carrera_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2942 (class 0 OID 0)
-- Dependencies: 502
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_carrera_postitulo_jurisdiccional_id_seq OWNED BY postitulos_estado_carrera_postitulo_jurisdiccional.id;


--
-- TOC entry 505 (class 1259 OID 22527)
-- Dependencies: 6
-- Name: postitulos_estado_normativa; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_normativa (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 504 (class 1259 OID 22525)
-- Dependencies: 505 6
-- Name: postitulos_estado_normativa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_normativa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2943 (class 0 OID 0)
-- Dependencies: 504
-- Name: postitulos_estado_normativa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_normativa_id_seq OWNED BY postitulos_estado_normativa.id;


--
-- TOC entry 489 (class 1259 OID 22401)
-- Dependencies: 6
-- Name: postitulos_estado_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 488 (class 1259 OID 22399)
-- Dependencies: 6 489
-- Name: postitulos_estado_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2944 (class 0 OID 0)
-- Dependencies: 488
-- Name: postitulos_estado_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_postitulo_id_seq OWNED BY postitulos_estado_postitulo.id;


--
-- TOC entry 515 (class 1259 OID 22618)
-- Dependencies: 6
-- Name: postitulos_estado_postitulo_nacional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_postitulo_nacional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 514 (class 1259 OID 22616)
-- Dependencies: 6 515
-- Name: postitulos_estado_postitulo_nacional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_postitulo_nacional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2945 (class 0 OID 0)
-- Dependencies: 514
-- Name: postitulos_estado_postitulo_nacional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_postitulo_nacional_id_seq OWNED BY postitulos_estado_postitulo_nacional.id;


--
-- TOC entry 507 (class 1259 OID 22537)
-- Dependencies: 6
-- Name: postitulos_normativa; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa (
    id integer NOT NULL,
    numero character varying(50) NOT NULL,
    descripcion character varying(255) NOT NULL,
    observaciones character varying(255),
    estado_id integer NOT NULL,
    fecha_alta date NOT NULL
);


--
-- TOC entry 506 (class 1259 OID 22535)
-- Dependencies: 507 6
-- Name: postitulos_normativa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2946 (class 0 OID 0)
-- Dependencies: 506
-- Name: postitulos_normativa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_id_seq OWNED BY postitulos_normativa.id;


--
-- TOC entry 525 (class 1259 OID 22707)
-- Dependencies: 6
-- Name: postitulos_normativa_postitulos_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa_postitulos_estados (
    id integer NOT NULL,
    normativa_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 524 (class 1259 OID 22705)
-- Dependencies: 525 6
-- Name: postitulos_normativa_postitulos_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_postitulos_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2947 (class 0 OID 0)
-- Dependencies: 524
-- Name: postitulos_normativa_postitulos_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_postitulos_estados_id_seq OWNED BY postitulos_normativa_postitulos_estados.id;


--
-- TOC entry 501 (class 1259 OID 22476)
-- Dependencies: 6
-- Name: postitulos_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulo (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    tipo_normativa_id integer NOT NULL,
    normativa character varying(50) NOT NULL,
    carrera_postitulo_id integer NOT NULL,
    observaciones character varying(255),
    estado_id integer NOT NULL
);


--
-- TOC entry 517 (class 1259 OID 22628)
-- Dependencies: 6
-- Name: postitulos_postitulo_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulo_estados (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 516 (class 1259 OID 22626)
-- Dependencies: 517 6
-- Name: postitulos_postitulo_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2948 (class 0 OID 0)
-- Dependencies: 516
-- Name: postitulos_postitulo_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_estados_id_seq OWNED BY postitulos_postitulo_estados.id;


--
-- TOC entry 500 (class 1259 OID 22474)
-- Dependencies: 6 501
-- Name: postitulos_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2949 (class 0 OID 0)
-- Dependencies: 500
-- Name: postitulos_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_id_seq OWNED BY postitulos_postitulo.id;


--
-- TOC entry 521 (class 1259 OID 22661)
-- Dependencies: 6
-- Name: postitulos_postitulo_nacional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulo_nacional (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    normativa_postitulo_id integer NOT NULL,
    estado_id integer NOT NULL,
    observaciones character varying(255),
    fecha_alta date NOT NULL
);


--
-- TOC entry 523 (class 1259 OID 22689)
-- Dependencies: 6
-- Name: postitulos_postitulo_nacional_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulo_nacional_estados (
    id integer NOT NULL,
    postitulo_nacional_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 522 (class 1259 OID 22687)
-- Dependencies: 523 6
-- Name: postitulos_postitulo_nacional_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_nacional_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2950 (class 0 OID 0)
-- Dependencies: 522
-- Name: postitulos_postitulo_nacional_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_nacional_estados_id_seq OWNED BY postitulos_postitulo_nacional_estados.id;


--
-- TOC entry 520 (class 1259 OID 22659)
-- Dependencies: 521 6
-- Name: postitulos_postitulo_nacional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_nacional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2951 (class 0 OID 0)
-- Dependencies: 520
-- Name: postitulos_postitulo_nacional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_nacional_id_seq OWNED BY postitulos_postitulo_nacional.id;


--
-- TOC entry 499 (class 1259 OID 22461)
-- Dependencies: 6
-- Name: postitulos_postitulos_areas; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_areas (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    areapostitulo_id integer NOT NULL
);


--
-- TOC entry 498 (class 1259 OID 22459)
-- Dependencies: 499 6
-- Name: postitulos_postitulos_areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_areas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2952 (class 0 OID 0)
-- Dependencies: 498
-- Name: postitulos_postitulos_areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_areas_id_seq OWNED BY postitulos_postitulos_areas.id;


--
-- TOC entry 495 (class 1259 OID 22431)
-- Dependencies: 6
-- Name: postitulos_postitulos_jurisdicciones; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_jurisdicciones (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL
);


--
-- TOC entry 494 (class 1259 OID 22429)
-- Dependencies: 495 6
-- Name: postitulos_postitulos_jurisdicciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_jurisdicciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2953 (class 0 OID 0)
-- Dependencies: 494
-- Name: postitulos_postitulos_jurisdicciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_jurisdicciones_id_seq OWNED BY postitulos_postitulos_jurisdicciones.id;


--
-- TOC entry 519 (class 1259 OID 22646)
-- Dependencies: 6
-- Name: postitulos_postitulos_nacionales_carreras; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_nacionales_carreras (
    id integer NOT NULL,
    postitulonacional_id integer NOT NULL,
    carrerapostitulo_id integer NOT NULL
);


--
-- TOC entry 518 (class 1259 OID 22644)
-- Dependencies: 6 519
-- Name: postitulos_postitulos_nacionales_carreras_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_nacionales_carreras_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2954 (class 0 OID 0)
-- Dependencies: 518
-- Name: postitulos_postitulos_nacionales_carreras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_nacionales_carreras_id_seq OWNED BY postitulos_postitulos_nacionales_carreras.id;


--
-- TOC entry 497 (class 1259 OID 22446)
-- Dependencies: 6
-- Name: postitulos_postitulos_niveles; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_niveles (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    nivel_id integer NOT NULL
);


--
-- TOC entry 496 (class 1259 OID 22444)
-- Dependencies: 497 6
-- Name: postitulos_postitulos_niveles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_niveles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2955 (class 0 OID 0)
-- Dependencies: 496
-- Name: postitulos_postitulos_niveles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_niveles_id_seq OWNED BY postitulos_postitulos_niveles.id;


--
-- TOC entry 493 (class 1259 OID 22421)
-- Dependencies: 6
-- Name: postitulos_tipo_normativa; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_tipo_normativa (
    id integer NOT NULL,
    descripcion character varying(50) NOT NULL
);


--
-- TOC entry 492 (class 1259 OID 22419)
-- Dependencies: 493 6
-- Name: postitulos_tipo_normativa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_tipo_normativa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2956 (class 0 OID 0)
-- Dependencies: 492
-- Name: postitulos_tipo_normativa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_tipo_normativa_id_seq OWNED BY postitulos_tipo_normativa.id;


--
-- TOC entry 491 (class 1259 OID 22411)
-- Dependencies: 6
-- Name: postitulos_tipo_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_tipo_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 490 (class 1259 OID 22409)
-- Dependencies: 6 491
-- Name: postitulos_tipo_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_tipo_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 2957 (class 0 OID 0)
-- Dependencies: 490
-- Name: postitulos_tipo_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_tipo_postitulo_id_seq OWNED BY postitulos_tipo_postitulo.id;


--
-- TOC entry 2771 (class 2604 OID 22386)
-- Dependencies: 486 487 487
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_estados_id_seq'::regclass);


--
-- TOC entry 2783 (class 2604 OID 22573)
-- Dependencies: 511 510 511
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2784 (class 2604 OID 22603)
-- Dependencies: 513 512 513
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_jurisdiccional_estados_id_seq'::regclass);


--
-- TOC entry 2770 (class 2604 OID 22365)
-- Dependencies: 484 485 485
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrerapostitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_carrerapostitulo_id_seq'::regclass);


--
-- TOC entry 2769 (class 2604 OID 22350)
-- Dependencies: 482 483 483
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones ALTER COLUMN id SET DEFAULT nextval('postitulos_carreras_postitulo_jurisdicciones_id_seq'::regclass);


--
-- TOC entry 2782 (class 2604 OID 22558)
-- Dependencies: 509 508 509
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas ALTER COLUMN id SET DEFAULT nextval('postitulos_carreras_postitulos_normativas_id_seq'::regclass);


--
-- TOC entry 2768 (class 2604 OID 22340)
-- Dependencies: 481 480 481
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_carrera_postitulo_id_seq'::regclass);


--
-- TOC entry 2779 (class 2604 OID 22520)
-- Dependencies: 503 502 503
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_carrera_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2780 (class 2604 OID 22530)
-- Dependencies: 505 504 505
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_normativa ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_normativa_id_seq'::regclass);


--
-- TOC entry 2772 (class 2604 OID 22404)
-- Dependencies: 489 488 489
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_postitulo_id_seq'::regclass);


--
-- TOC entry 2785 (class 2604 OID 22621)
-- Dependencies: 514 515 515
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_postitulo_nacional_id_seq'::regclass);


--
-- TOC entry 2781 (class 2604 OID 22540)
-- Dependencies: 507 506 507
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_id_seq'::regclass);


--
-- TOC entry 2790 (class 2604 OID 22710)
-- Dependencies: 524 525 525
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_postitulos_estados_id_seq'::regclass);


--
-- TOC entry 2778 (class 2604 OID 22479)
-- Dependencies: 500 501 501
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_id_seq'::regclass);


--
-- TOC entry 2786 (class 2604 OID 22631)
-- Dependencies: 517 516 517
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_estados_id_seq'::regclass);


--
-- TOC entry 2788 (class 2604 OID 22664)
-- Dependencies: 521 520 521
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_nacional_id_seq'::regclass);


--
-- TOC entry 2789 (class 2604 OID 22692)
-- Dependencies: 522 523 523
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_nacional_estados_id_seq'::regclass);


--
-- TOC entry 2777 (class 2604 OID 22464)
-- Dependencies: 498 499 499
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_areas_id_seq'::regclass);


--
-- TOC entry 2775 (class 2604 OID 22434)
-- Dependencies: 495 494 495
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_jurisdicciones_id_seq'::regclass);


--
-- TOC entry 2787 (class 2604 OID 22649)
-- Dependencies: 518 519 519
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_nacionales_carreras_id_seq'::regclass);


--
-- TOC entry 2776 (class 2604 OID 22449)
-- Dependencies: 497 496 497
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_niveles_id_seq'::regclass);


--
-- TOC entry 2774 (class 2604 OID 22424)
-- Dependencies: 493 492 493
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_tipo_normativa ALTER COLUMN id SET DEFAULT nextval('postitulos_tipo_normativa_id_seq'::regclass);


--
-- TOC entry 2773 (class 2604 OID 22414)
-- Dependencies: 490 491 491
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_tipo_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_tipo_postitulo_id_seq'::regclass);


--
-- TOC entry 2807 (class 2606 OID 22388)
-- Dependencies: 487 487
-- Name: postitulos_carrera_postitulo_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 2863 (class 2606 OID 22577)
-- Dependencies: 511 511 511
-- Name: postitulos_carrera_postitulo_jurisdicc_carrera_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdicc_carrera_postitulo_id_key UNIQUE (carrera_postitulo_id, jurisdiccion_id);


--
-- TOC entry 2872 (class 2606 OID 22605)
-- Dependencies: 513 513
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 2868 (class 2606 OID 22575)
-- Dependencies: 511 511
-- Name: postitulos_carrera_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2803 (class 2606 OID 22370)
-- Dependencies: 485 485
-- Name: postitulos_carrerapostitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrerapostitulo
    ADD CONSTRAINT postitulos_carrerapostitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2857 (class 2606 OID 22562)
-- Dependencies: 509 509 509
-- Name: postitulos_carreras_postitulo_carrerapostitulojurisdicciona_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulo_carrerapostitulojurisdicciona_key UNIQUE (carrerapostitulojurisdiccional_id, normativapostitulo_id);


--
-- TOC entry 2796 (class 2606 OID 22354)
-- Dependencies: 483 483 483
-- Name: postitulos_carreras_postitulo_jurisdicc_carrerapostitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_jurisdicc_carrerapostitulo_id_key UNIQUE (carrerapostitulo_id, jurisdiccion_id);


--
-- TOC entry 2800 (class 2606 OID 22352)
-- Dependencies: 483 483
-- Name: postitulos_carreras_postitulo_jurisdicciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_jurisdicciones_pkey PRIMARY KEY (id);


--
-- TOC entry 2861 (class 2606 OID 22560)
-- Dependencies: 509 509
-- Name: postitulos_carreras_postitulos_normativas_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulos_normativas_pkey PRIMARY KEY (id);


--
-- TOC entry 2844 (class 2606 OID 22524)
-- Dependencies: 503 503
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_jurisdiccional_nombre_key UNIQUE (nombre);


--
-- TOC entry 2846 (class 2606 OID 22522)
-- Dependencies: 503 503
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2792 (class 2606 OID 22344)
-- Dependencies: 481 481
-- Name: postitulos_estado_carrera_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2794 (class 2606 OID 22342)
-- Dependencies: 481 481
-- Name: postitulos_estado_carrera_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2848 (class 2606 OID 22534)
-- Dependencies: 505 505
-- Name: postitulos_estado_normativa_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa
    ADD CONSTRAINT postitulos_estado_normativa_nombre_key UNIQUE (nombre);


--
-- TOC entry 2850 (class 2606 OID 22532)
-- Dependencies: 505 505
-- Name: postitulos_estado_normativa_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa
    ADD CONSTRAINT postitulos_estado_normativa_pkey PRIMARY KEY (id);


--
-- TOC entry 2874 (class 2606 OID 22625)
-- Dependencies: 515 515
-- Name: postitulos_estado_postitulo_nacional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional
    ADD CONSTRAINT postitulos_estado_postitulo_nacional_nombre_key UNIQUE (nombre);


--
-- TOC entry 2876 (class 2606 OID 22623)
-- Dependencies: 515 515
-- Name: postitulos_estado_postitulo_nacional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional
    ADD CONSTRAINT postitulos_estado_postitulo_nacional_pkey PRIMARY KEY (id);


--
-- TOC entry 2809 (class 2606 OID 22408)
-- Dependencies: 489 489
-- Name: postitulos_estado_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo
    ADD CONSTRAINT postitulos_estado_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2811 (class 2606 OID 22406)
-- Dependencies: 489 489
-- Name: postitulos_estado_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo
    ADD CONSTRAINT postitulos_estado_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2853 (class 2606 OID 22547)
-- Dependencies: 507 507
-- Name: postitulos_normativa_numero_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_numero_key UNIQUE (numero);


--
-- TOC entry 2855 (class 2606 OID 22545)
-- Dependencies: 507 507
-- Name: postitulos_normativa_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_pkey PRIMARY KEY (id);


--
-- TOC entry 2900 (class 2606 OID 22712)
-- Dependencies: 525 525
-- Name: postitulos_normativa_postitulos_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 2879 (class 2606 OID 22633)
-- Dependencies: 517 517
-- Name: postitulos_postitulo_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 2895 (class 2606 OID 22694)
-- Dependencies: 523 523
-- Name: postitulos_postitulo_nacional_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 2889 (class 2606 OID 22671)
-- Dependencies: 521 521 521
-- Name: postitulos_postitulo_nacional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_nombre_key UNIQUE (nombre, normativa_postitulo_id);


--
-- TOC entry 2892 (class 2606 OID 22669)
-- Dependencies: 521 521
-- Name: postitulos_postitulo_nacional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_pkey PRIMARY KEY (id);


--
-- TOC entry 2841 (class 2606 OID 22484)
-- Dependencies: 501 501
-- Name: postitulos_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2834 (class 2606 OID 22466)
-- Dependencies: 499 499
-- Name: postitulos_postitulos_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_pkey PRIMARY KEY (id);


--
-- TOC entry 2837 (class 2606 OID 22468)
-- Dependencies: 499 499 499
-- Name: postitulos_postitulos_areas_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_postitulo_id_key UNIQUE (postitulo_id, areapostitulo_id);


--
-- TOC entry 2822 (class 2606 OID 22436)
-- Dependencies: 495 495
-- Name: postitulos_postitulos_jurisdicciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdicciones_pkey PRIMARY KEY (id);


--
-- TOC entry 2825 (class 2606 OID 22438)
-- Dependencies: 495 495 495
-- Name: postitulos_postitulos_jurisdicciones_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdicciones_postitulo_id_key UNIQUE (postitulo_id, jurisdiccion_id);


--
-- TOC entry 2882 (class 2606 OID 22653)
-- Dependencies: 519 519 519
-- Name: postitulos_postitulos_nacionales_carre_postitulonacional_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_nacionales_carre_postitulonacional_id_key UNIQUE (postitulonacional_id, carrerapostitulo_id);


--
-- TOC entry 2885 (class 2606 OID 22651)
-- Dependencies: 519 519
-- Name: postitulos_postitulos_nacionales_carreras_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_nacionales_carreras_pkey PRIMARY KEY (id);


--
-- TOC entry 2828 (class 2606 OID 22451)
-- Dependencies: 497 497
-- Name: postitulos_postitulos_niveles_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_pkey PRIMARY KEY (id);


--
-- TOC entry 2831 (class 2606 OID 22453)
-- Dependencies: 497 497 497
-- Name: postitulos_postitulos_niveles_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_postitulo_id_key UNIQUE (postitulo_id, nivel_id);


--
-- TOC entry 2817 (class 2606 OID 22428)
-- Dependencies: 493 493
-- Name: postitulos_tipo_normativa_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa
    ADD CONSTRAINT postitulos_tipo_normativa_descripcion_key UNIQUE (descripcion);


--
-- TOC entry 2819 (class 2606 OID 22426)
-- Dependencies: 493 493
-- Name: postitulos_tipo_normativa_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa
    ADD CONSTRAINT postitulos_tipo_normativa_pkey PRIMARY KEY (id);


--
-- TOC entry 2813 (class 2606 OID 22418)
-- Dependencies: 491 491
-- Name: postitulos_tipo_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_postitulo
    ADD CONSTRAINT postitulos_tipo_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2815 (class 2606 OID 22416)
-- Dependencies: 491 491
-- Name: postitulos_tipo_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_postitulo
    ADD CONSTRAINT postitulos_tipo_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2804 (class 1259 OID 22726)
-- Dependencies: 487
-- Name: postitulos_carrera_postitulo_estados_carrera_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_estados_carrera_postitulo_id ON postitulos_carrera_postitulo_estados USING btree (carrera_postitulo_id);


--
-- TOC entry 2805 (class 1259 OID 22727)
-- Dependencies: 487
-- Name: postitulos_carrera_postitulo_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_estados_estado_id ON postitulos_carrera_postitulo_estados USING btree (estado_id);


--
-- TOC entry 2864 (class 1259 OID 22740)
-- Dependencies: 511
-- Name: postitulos_carrera_postitulo_jurisdiccional_carrera_postitulo_i; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_carrera_postitulo_i ON postitulos_carrera_postitulo_jurisdiccional USING btree (carrera_postitulo_id);


--
-- TOC entry 2865 (class 1259 OID 22742)
-- Dependencies: 511
-- Name: postitulos_carrera_postitulo_jurisdiccional_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estado_id ON postitulos_carrera_postitulo_jurisdiccional USING btree (estado_id);


--
-- TOC entry 2869 (class 1259 OID 22743)
-- Dependencies: 513
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_carrera_pos; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estados_carrera_pos ON postitulos_carrera_postitulo_jurisdiccional_estados USING btree (carrera_postitulo_jurisdiccional_id);


--
-- TOC entry 2870 (class 1259 OID 22744)
-- Dependencies: 513
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estados_estado_id ON postitulos_carrera_postitulo_jurisdiccional_estados USING btree (estado_id);


--
-- TOC entry 2866 (class 1259 OID 22741)
-- Dependencies: 511
-- Name: postitulos_carrera_postitulo_jurisdiccional_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_jurisdiccion_id ON postitulos_carrera_postitulo_jurisdiccional USING btree (jurisdiccion_id);


--
-- TOC entry 2801 (class 1259 OID 22725)
-- Dependencies: 485
-- Name: postitulos_carrerapostitulo_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrerapostitulo_estado_id ON postitulos_carrerapostitulo USING btree (estado_id);


--
-- TOC entry 2797 (class 1259 OID 22723)
-- Dependencies: 483
-- Name: postitulos_carreras_postitulo_jurisdicciones_carrerapostitulo_i; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulo_jurisdicciones_carrerapostitulo_i ON postitulos_carreras_postitulo_jurisdicciones USING btree (carrerapostitulo_id);


--
-- TOC entry 2798 (class 1259 OID 22724)
-- Dependencies: 483
-- Name: postitulos_carreras_postitulo_jurisdicciones_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulo_jurisdicciones_jurisdiccion_id ON postitulos_carreras_postitulo_jurisdicciones USING btree (jurisdiccion_id);


--
-- TOC entry 2858 (class 1259 OID 22738)
-- Dependencies: 509
-- Name: postitulos_carreras_postitulos_normativas_carrerapostitulojuris; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulos_normativas_carrerapostitulojuris ON postitulos_carreras_postitulos_normativas USING btree (carrerapostitulojurisdiccional_id);


--
-- TOC entry 2859 (class 1259 OID 22739)
-- Dependencies: 509
-- Name: postitulos_carreras_postitulos_normativas_normativapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulos_normativas_normativapostitulo_id ON postitulos_carreras_postitulos_normativas USING btree (normativapostitulo_id);


--
-- TOC entry 2851 (class 1259 OID 22737)
-- Dependencies: 507
-- Name: postitulos_normativa_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_estado_id ON postitulos_normativa USING btree (estado_id);


--
-- TOC entry 2897 (class 1259 OID 22754)
-- Dependencies: 525
-- Name: postitulos_normativa_postitulos_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulos_estados_estado_id ON postitulos_normativa_postitulos_estados USING btree (estado_id);


--
-- TOC entry 2898 (class 1259 OID 22753)
-- Dependencies: 525
-- Name: postitulos_normativa_postitulos_estados_normativa_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulos_estados_normativa_id ON postitulos_normativa_postitulos_estados USING btree (normativa_id);


--
-- TOC entry 2838 (class 1259 OID 22735)
-- Dependencies: 501
-- Name: postitulos_postitulo_carrera_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_carrera_postitulo_id ON postitulos_postitulo USING btree (carrera_postitulo_id);


--
-- TOC entry 2839 (class 1259 OID 22736)
-- Dependencies: 501
-- Name: postitulos_postitulo_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estado_id ON postitulos_postitulo USING btree (estado_id);


--
-- TOC entry 2877 (class 1259 OID 22746)
-- Dependencies: 517
-- Name: postitulos_postitulo_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estados_estado_id ON postitulos_postitulo_estados USING btree (estado_id);


--
-- TOC entry 2880 (class 1259 OID 22745)
-- Dependencies: 517
-- Name: postitulos_postitulo_estados_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estados_postitulo_id ON postitulos_postitulo_estados USING btree (postitulo_id);


--
-- TOC entry 2887 (class 1259 OID 22750)
-- Dependencies: 521
-- Name: postitulos_postitulo_nacional_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estado_id ON postitulos_postitulo_nacional USING btree (estado_id);


--
-- TOC entry 2893 (class 1259 OID 22752)
-- Dependencies: 523
-- Name: postitulos_postitulo_nacional_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estados_estado_id ON postitulos_postitulo_nacional_estados USING btree (estado_id);


--
-- TOC entry 2896 (class 1259 OID 22751)
-- Dependencies: 523
-- Name: postitulos_postitulo_nacional_estados_postitulo_nacional_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estados_postitulo_nacional_id ON postitulos_postitulo_nacional_estados USING btree (postitulo_nacional_id);


--
-- TOC entry 2890 (class 1259 OID 22749)
-- Dependencies: 521
-- Name: postitulos_postitulo_nacional_normativa_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_normativa_postitulo_id ON postitulos_postitulo_nacional USING btree (normativa_postitulo_id);


--
-- TOC entry 2842 (class 1259 OID 22734)
-- Dependencies: 501
-- Name: postitulos_postitulo_tipo_normativa_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_tipo_normativa_id ON postitulos_postitulo USING btree (tipo_normativa_id);


--
-- TOC entry 2832 (class 1259 OID 22733)
-- Dependencies: 499
-- Name: postitulos_postitulos_areas_areapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_areas_areapostitulo_id ON postitulos_postitulos_areas USING btree (areapostitulo_id);


--
-- TOC entry 2835 (class 1259 OID 22732)
-- Dependencies: 499
-- Name: postitulos_postitulos_areas_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_areas_postitulo_id ON postitulos_postitulos_areas USING btree (postitulo_id);


--
-- TOC entry 2820 (class 1259 OID 22729)
-- Dependencies: 495
-- Name: postitulos_postitulos_jurisdicciones_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_jurisdicciones_jurisdiccion_id ON postitulos_postitulos_jurisdicciones USING btree (jurisdiccion_id);


--
-- TOC entry 2823 (class 1259 OID 22728)
-- Dependencies: 495
-- Name: postitulos_postitulos_jurisdicciones_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_jurisdicciones_postitulo_id ON postitulos_postitulos_jurisdicciones USING btree (postitulo_id);


--
-- TOC entry 2883 (class 1259 OID 22748)
-- Dependencies: 519
-- Name: postitulos_postitulos_nacionales_carreras_carrerapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_nacionales_carreras_carrerapostitulo_id ON postitulos_postitulos_nacionales_carreras USING btree (carrerapostitulo_id);


--
-- TOC entry 2886 (class 1259 OID 22747)
-- Dependencies: 519
-- Name: postitulos_postitulos_nacionales_carreras_postitulonacional_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_nacionales_carreras_postitulonacional_id ON postitulos_postitulos_nacionales_carreras USING btree (postitulonacional_id);


--
-- TOC entry 2826 (class 1259 OID 22731)
-- Dependencies: 497
-- Name: postitulos_postitulos_niveles_nivel_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_niveles_nivel_id ON postitulos_postitulos_niveles USING btree (nivel_id);


--
-- TOC entry 2829 (class 1259 OID 22730)
-- Dependencies: 497
-- Name: postitulos_postitulos_niveles_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_niveles_postitulo_id ON postitulos_postitulos_niveles USING btree (postitulo_id);


--
-- TOC entry 2902 (class 2606 OID 22376)
-- Dependencies: 483 485 2802
-- Name: carrerapostitulo_id_refs_id_5048cd6d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT carrerapostitulo_id_refs_id_5048cd6d FOREIGN KEY (carrerapostitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2917 (class 2606 OID 22593)
-- Dependencies: 2867 509 511
-- Name: carrerapostitulojurisdiccional_id_refs_id_f1944112; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT carrerapostitulojurisdiccional_id_refs_id_f1944112 FOREIGN KEY (carrerapostitulojurisdiccional_id) REFERENCES postitulos_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2911 (class 2606 OID 22510)
-- Dependencies: 499 2840 501
-- Name: postitulo_id_refs_id_411f3970; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulo_id_refs_id_411f3970 FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2909 (class 2606 OID 22505)
-- Dependencies: 501 497 2840
-- Name: postitulo_id_refs_id_c623075c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulo_id_refs_id_c623075c FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2907 (class 2606 OID 22500)
-- Dependencies: 2840 495 501
-- Name: postitulo_id_refs_id_cc7be725; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulo_id_refs_id_cc7be725 FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2926 (class 2606 OID 22682)
-- Dependencies: 2891 519 521
-- Name: postitulonacional_id_refs_id_f0dcbf7c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulonacional_id_refs_id_f0dcbf7c FOREIGN KEY (postitulonacional_id) REFERENCES postitulos_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2921 (class 2606 OID 22606)
-- Dependencies: 2867 513 511
-- Name: postitulos_carrera_postitulo__carrera_postitulo_jurisdicci_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo__carrera_postitulo_jurisdicci_fkey FOREIGN KEY (carrera_postitulo_jurisdiccional_id) REFERENCES postitulos_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2904 (class 2606 OID 22389)
-- Dependencies: 485 2802 487
-- Name: postitulos_carrera_postitulo_estados_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2905 (class 2606 OID 22394)
-- Dependencies: 2793 481 487
-- Name: postitulos_carrera_postitulo_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2918 (class 2606 OID 22578)
-- Dependencies: 2802 485 511
-- Name: postitulos_carrera_postitulo_jurisdic_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdic_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2919 (class 2606 OID 22583)
-- Dependencies: 511 284
-- Name: postitulos_carrera_postitulo_jurisdicciona_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdicciona_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2922 (class 2606 OID 22611)
-- Dependencies: 2845 513 503
-- Name: postitulos_carrera_postitulo_jurisdiccional_esta_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_esta_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2920 (class 2606 OID 22588)
-- Dependencies: 2845 511 503
-- Name: postitulos_carrera_postitulo_jurisdiccional_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2903 (class 2606 OID 22371)
-- Dependencies: 481 485 2793
-- Name: postitulos_carrerapostitulo_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrerapostitulo
    ADD CONSTRAINT postitulos_carrerapostitulo_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2901 (class 2606 OID 22355)
-- Dependencies: 483 284
-- Name: postitulos_carreras_postitulo_jurisdiccion_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_jurisdiccion_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2916 (class 2606 OID 22563)
-- Dependencies: 2854 509 507
-- Name: postitulos_carreras_postitulos_norma_normativapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulos_norma_normativapostitulo_id_fkey FOREIGN KEY (normativapostitulo_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2915 (class 2606 OID 22548)
-- Dependencies: 2849 505 507
-- Name: postitulos_normativa_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2932 (class 2606 OID 22718)
-- Dependencies: 2849 505 525
-- Name: postitulos_normativa_postitulos_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2931 (class 2606 OID 22713)
-- Dependencies: 2854 507 525
-- Name: postitulos_normativa_postitulos_estados_normativa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_estados_normativa_id_fkey FOREIGN KEY (normativa_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2913 (class 2606 OID 22490)
-- Dependencies: 2802 485 501
-- Name: postitulos_postitulo_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2914 (class 2606 OID 22495)
-- Dependencies: 2810 489 501
-- Name: postitulos_postitulo_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2924 (class 2606 OID 22639)
-- Dependencies: 517 2810 489
-- Name: postitulos_postitulo_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2923 (class 2606 OID 22634)
-- Dependencies: 517 2840 501
-- Name: postitulos_postitulo_estados_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_postitulo_id_fkey FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2928 (class 2606 OID 22677)
-- Dependencies: 2875 521 515
-- Name: postitulos_postitulo_nacional_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2929 (class 2606 OID 22695)
-- Dependencies: 523 2891 521
-- Name: postitulos_postitulo_nacional_estado_postitulo_nacional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estado_postitulo_nacional_id_fkey FOREIGN KEY (postitulo_nacional_id) REFERENCES postitulos_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2930 (class 2606 OID 22700)
-- Dependencies: 523 515 2875
-- Name: postitulos_postitulo_nacional_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2927 (class 2606 OID 22672)
-- Dependencies: 521 2854 507
-- Name: postitulos_postitulo_nacional_normativa_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_normativa_postitulo_id_fkey FOREIGN KEY (normativa_postitulo_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2912 (class 2606 OID 22485)
-- Dependencies: 501 2818 493
-- Name: postitulos_postitulo_tipo_normativa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_tipo_normativa_id_fkey FOREIGN KEY (tipo_normativa_id) REFERENCES postitulos_tipo_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2910 (class 2606 OID 22469)
-- Dependencies: 499 479
-- Name: postitulos_postitulos_areas_areapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_areapostitulo_id_fkey FOREIGN KEY (areapostitulo_id) REFERENCES postitulos_area_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2906 (class 2606 OID 22439)
-- Dependencies: 284 495
-- Name: postitulos_postitulos_jurisdicciones_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdicciones_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2925 (class 2606 OID 22654)
-- Dependencies: 519 485 2802
-- Name: postitulos_postitulos_nacionales_carre_carrerapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_nacionales_carre_carrerapostitulo_id_fkey FOREIGN KEY (carrerapostitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2908 (class 2606 OID 22454)
-- Dependencies: 497 288
-- Name: postitulos_postitulos_niveles_nivel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_nivel_id_fkey FOREIGN KEY (nivel_id) REFERENCES registro_nivel(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2014-05-25 23:19:59 ART

--
-- PostgreSQL database dump complete
--

-----------------------
INSERT INTO postitulos_estado_carrera_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_postitulo_nacional (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_normativa (nombre) VALUES ('Vigente'), ('No vigente');
-----------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('132', 'Postítulos', 'Aplicación de postítulos - #406');

COMMIT;
