BEGIN;

--
INSERT INTO seguridad_aplicacion (nombre, descripcion, home_url) VALUES ('Postítulos', 'Postítulos', '/postitulos/');

-- SCHEMA DUMP ACA
--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.13
-- Dumped by pg_dump version 9.1.13
-- Started on 2014-06-02 15:00:49 ART

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 500 (class 1259 OID 190914)
-- Dependencies: 6
-- Name: postitulos_area_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_area_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 499 (class 1259 OID 190912)
-- Dependencies: 500 6
-- Name: postitulos_area_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_area_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3307 (class 0 OID 0)
-- Dependencies: 499
-- Name: postitulos_area_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_area_postitulo_id_seq OWNED BY postitulos_area_postitulo.id;


--
-- TOC entry 508 (class 1259 OID 190970)
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
-- TOC entry 507 (class 1259 OID 190968)
-- Dependencies: 508 6
-- Name: postitulos_carrera_postitulo_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3308 (class 0 OID 0)
-- Dependencies: 507
-- Name: postitulos_carrera_postitulo_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_estados_id_seq OWNED BY postitulos_carrera_postitulo_estados.id;


--
-- TOC entry 532 (class 1259 OID 191157)
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
-- TOC entry 534 (class 1259 OID 191187)
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
-- TOC entry 533 (class 1259 OID 191185)
-- Dependencies: 534 6
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_jurisdiccional_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3309 (class 0 OID 0)
-- Dependencies: 533
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_jurisdiccional_estados_id_seq OWNED BY postitulos_carrera_postitulo_jurisdiccional_estados.id;


--
-- TOC entry 531 (class 1259 OID 191155)
-- Dependencies: 532 6
-- Name: postitulos_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrera_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3310 (class 0 OID 0)
-- Dependencies: 531
-- Name: postitulos_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrera_postitulo_jurisdiccional_id_seq OWNED BY postitulos_carrera_postitulo_jurisdiccional.id;


--
-- TOC entry 506 (class 1259 OID 190949)
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
-- TOC entry 505 (class 1259 OID 190947)
-- Dependencies: 506 6
-- Name: postitulos_carrerapostitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carrerapostitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3311 (class 0 OID 0)
-- Dependencies: 505
-- Name: postitulos_carrerapostitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carrerapostitulo_id_seq OWNED BY postitulos_carrerapostitulo.id;


--
-- TOC entry 504 (class 1259 OID 190934)
-- Dependencies: 6
-- Name: postitulos_carreras_postitulo_jurisdicciones; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carreras_postitulo_jurisdicciones (
    id integer NOT NULL,
    carrerapostitulo_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL
);


--
-- TOC entry 503 (class 1259 OID 190932)
-- Dependencies: 504 6
-- Name: postitulos_carreras_postitulo_jurisdicciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carreras_postitulo_jurisdicciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3312 (class 0 OID 0)
-- Dependencies: 503
-- Name: postitulos_carreras_postitulo_jurisdicciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carreras_postitulo_jurisdicciones_id_seq OWNED BY postitulos_carreras_postitulo_jurisdicciones.id;


--
-- TOC entry 530 (class 1259 OID 191142)
-- Dependencies: 6
-- Name: postitulos_carreras_postitulos_normativas; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_carreras_postitulos_normativas (
    id integer NOT NULL,
    carrerapostitulojurisdiccional_id integer NOT NULL,
    normativapostitulo_id integer NOT NULL
);


--
-- TOC entry 529 (class 1259 OID 191140)
-- Dependencies: 530 6
-- Name: postitulos_carreras_postitulos_normativas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_carreras_postitulos_normativas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3313 (class 0 OID 0)
-- Dependencies: 529
-- Name: postitulos_carreras_postitulos_normativas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_carreras_postitulos_normativas_id_seq OWNED BY postitulos_carreras_postitulos_normativas.id;


--
-- TOC entry 570 (class 1259 OID 191505)
-- Dependencies: 2919 6
-- Name: postitulos_cohorte_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_cohorte_postitulo (
    id integer NOT NULL,
    carrera_postitulo_jurisdiccional_id integer NOT NULL,
    anio integer NOT NULL,
    observaciones character varying(255),
    revisado_jurisdiccion boolean,
    CONSTRAINT postitulos_cohorte_postitulo_anio_check CHECK ((anio >= 0))
);


--
-- TOC entry 569 (class 1259 OID 191503)
-- Dependencies: 570 6
-- Name: postitulos_cohorte_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_cohorte_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3314 (class 0 OID 0)
-- Dependencies: 569
-- Name: postitulos_cohorte_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_cohorte_postitulo_id_seq OWNED BY postitulos_cohorte_postitulo.id;


--
-- TOC entry 578 (class 1259 OID 191567)
-- Dependencies: 2925 6
-- Name: postitulos_cohortes_postitulo_anexos; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_cohortes_postitulo_anexos (
    id integer NOT NULL,
    anexo_id integer NOT NULL,
    cohorte_postitulo_id integer NOT NULL,
    inscriptos integer,
    estado_id integer NOT NULL,
    CONSTRAINT postitulos_cohortes_postitulo_anexos_inscriptos_check CHECK ((inscriptos >= 0))
);


--
-- TOC entry 577 (class 1259 OID 191565)
-- Dependencies: 578 6
-- Name: postitulos_cohortes_postitulo_anexos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_cohortes_postitulo_anexos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3315 (class 0 OID 0)
-- Dependencies: 577
-- Name: postitulos_cohortes_postitulo_anexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_cohortes_postitulo_anexos_id_seq OWNED BY postitulos_cohortes_postitulo_anexos.id;


--
-- TOC entry 574 (class 1259 OID 191531)
-- Dependencies: 2922 6
-- Name: postitulos_cohortes_postitulo_establecimientos; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_cohortes_postitulo_establecimientos (
    id integer NOT NULL,
    establecimiento_id integer NOT NULL,
    cohorte_postitulo_id integer NOT NULL,
    inscriptos integer,
    estado_id integer NOT NULL,
    CONSTRAINT postitulos_cohortes_postitulo_establecimientos_inscriptos_check CHECK ((inscriptos >= 0))
);


--
-- TOC entry 573 (class 1259 OID 191529)
-- Dependencies: 574 6
-- Name: postitulos_cohortes_postitulo_establecimientos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_cohortes_postitulo_establecimientos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3316 (class 0 OID 0)
-- Dependencies: 573
-- Name: postitulos_cohortes_postitulo_establecimientos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_cohortes_postitulo_establecimientos_id_seq OWNED BY postitulos_cohortes_postitulo_establecimientos.id;


--
-- TOC entry 582 (class 1259 OID 191603)
-- Dependencies: 2928 6
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_cohortes_postitulo_extensiones_aulicas (
    id integer NOT NULL,
    extension_aulica_id integer NOT NULL,
    cohorte_postitulo_id integer NOT NULL,
    inscriptos integer,
    estado_id integer NOT NULL,
    CONSTRAINT postitulos_cohortes_postitulo_extensiones_auli_inscriptos_check CHECK ((inscriptos >= 0))
);


--
-- TOC entry 581 (class 1259 OID 191601)
-- Dependencies: 582 6
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_cohortes_postitulo_extensiones_aulicas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3317 (class 0 OID 0)
-- Dependencies: 581
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_cohortes_postitulo_extensiones_aulicas_id_seq OWNED BY postitulos_cohortes_postitulo_extensiones_aulicas.id;


--
-- TOC entry 502 (class 1259 OID 190924)
-- Dependencies: 6
-- Name: postitulos_estado_carrera_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_carrera_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 501 (class 1259 OID 190922)
-- Dependencies: 502 6
-- Name: postitulos_estado_carrera_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_carrera_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3318 (class 0 OID 0)
-- Dependencies: 501
-- Name: postitulos_estado_carrera_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_carrera_postitulo_id_seq OWNED BY postitulos_estado_carrera_postitulo.id;


--
-- TOC entry 524 (class 1259 OID 191104)
-- Dependencies: 6
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_carrera_postitulo_jurisdiccional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 523 (class 1259 OID 191102)
-- Dependencies: 524 6
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_carrera_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3319 (class 0 OID 0)
-- Dependencies: 523
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_carrera_postitulo_jurisdiccional_id_seq OWNED BY postitulos_estado_carrera_postitulo_jurisdiccional.id;


--
-- TOC entry 576 (class 1259 OID 191557)
-- Dependencies: 6
-- Name: postitulos_estado_cohorte_postitulo_anexo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_cohorte_postitulo_anexo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 575 (class 1259 OID 191555)
-- Dependencies: 576 6
-- Name: postitulos_estado_cohorte_postitulo_anexo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_cohorte_postitulo_anexo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3320 (class 0 OID 0)
-- Dependencies: 575
-- Name: postitulos_estado_cohorte_postitulo_anexo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_cohorte_postitulo_anexo_id_seq OWNED BY postitulos_estado_cohorte_postitulo_anexo.id;


--
-- TOC entry 572 (class 1259 OID 191521)
-- Dependencies: 6
-- Name: postitulos_estado_cohorte_postitulo_establecimiento; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_cohorte_postitulo_establecimiento (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 571 (class 1259 OID 191519)
-- Dependencies: 572 6
-- Name: postitulos_estado_cohorte_postitulo_establecimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_cohorte_postitulo_establecimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3321 (class 0 OID 0)
-- Dependencies: 571
-- Name: postitulos_estado_cohorte_postitulo_establecimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_cohorte_postitulo_establecimiento_id_seq OWNED BY postitulos_estado_cohorte_postitulo_establecimiento.id;


--
-- TOC entry 580 (class 1259 OID 191593)
-- Dependencies: 6
-- Name: postitulos_estado_cohorte_postitulo_extension_aulica; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_cohorte_postitulo_extension_aulica (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 579 (class 1259 OID 191591)
-- Dependencies: 580 6
-- Name: postitulos_estado_cohorte_postitulo_extension_aulica_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_cohorte_postitulo_extension_aulica_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3322 (class 0 OID 0)
-- Dependencies: 579
-- Name: postitulos_estado_cohorte_postitulo_extension_aulica_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_cohorte_postitulo_extension_aulica_id_seq OWNED BY postitulos_estado_cohorte_postitulo_extension_aulica.id;


--
-- TOC entry 526 (class 1259 OID 191114)
-- Dependencies: 6
-- Name: postitulos_estado_normativa_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_normativa_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 525 (class 1259 OID 191112)
-- Dependencies: 526 6
-- Name: postitulos_estado_normativa_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_normativa_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3323 (class 0 OID 0)
-- Dependencies: 525
-- Name: postitulos_estado_normativa_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_normativa_postitulo_id_seq OWNED BY postitulos_estado_normativa_postitulo.id;


--
-- TOC entry 552 (class 1259 OID 191332)
-- Dependencies: 6
-- Name: postitulos_estado_normativa_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_normativa_postitulo_jurisdiccional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 551 (class 1259 OID 191330)
-- Dependencies: 552 6
-- Name: postitulos_estado_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_normativa_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3324 (class 0 OID 0)
-- Dependencies: 551
-- Name: postitulos_estado_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_normativa_postitulo_jurisdiccional_id_seq OWNED BY postitulos_estado_normativa_postitulo_jurisdiccional.id;


--
-- TOC entry 510 (class 1259 OID 190988)
-- Dependencies: 6
-- Name: postitulos_estado_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 509 (class 1259 OID 190986)
-- Dependencies: 510 6
-- Name: postitulos_estado_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3325 (class 0 OID 0)
-- Dependencies: 509
-- Name: postitulos_estado_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_postitulo_id_seq OWNED BY postitulos_estado_postitulo.id;


--
-- TOC entry 536 (class 1259 OID 191205)
-- Dependencies: 6
-- Name: postitulos_estado_postitulo_nacional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_postitulo_nacional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 535 (class 1259 OID 191203)
-- Dependencies: 536 6
-- Name: postitulos_estado_postitulo_nacional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_postitulo_nacional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3326 (class 0 OID 0)
-- Dependencies: 535
-- Name: postitulos_estado_postitulo_nacional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_postitulo_nacional_id_seq OWNED BY postitulos_estado_postitulo_nacional.id;


--
-- TOC entry 558 (class 1259 OID 191388)
-- Dependencies: 6
-- Name: postitulos_estado_solicitud; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_estado_solicitud (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 557 (class 1259 OID 191386)
-- Dependencies: 558 6
-- Name: postitulos_estado_solicitud_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_estado_solicitud_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3327 (class 0 OID 0)
-- Dependencies: 557
-- Name: postitulos_estado_solicitud_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_estado_solicitud_id_seq OWNED BY postitulos_estado_solicitud.id;


--
-- TOC entry 528 (class 1259 OID 191124)
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
-- TOC entry 527 (class 1259 OID 191122)
-- Dependencies: 528 6
-- Name: postitulos_normativa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3328 (class 0 OID 0)
-- Dependencies: 527
-- Name: postitulos_normativa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_id_seq OWNED BY postitulos_normativa.id;


--
-- TOC entry 550 (class 1259 OID 191322)
-- Dependencies: 6
-- Name: postitulos_normativa_motivo_otorgamiento; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa_motivo_otorgamiento (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 549 (class 1259 OID 191320)
-- Dependencies: 550 6
-- Name: postitulos_normativa_motivo_otorgamiento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_motivo_otorgamiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3329 (class 0 OID 0)
-- Dependencies: 549
-- Name: postitulos_normativa_motivo_otorgamiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_motivo_otorgamiento_id_seq OWNED BY postitulos_normativa_motivo_otorgamiento.id;


--
-- TOC entry 554 (class 1259 OID 191342)
-- Dependencies: 6
-- Name: postitulos_normativa_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa_postitulo_jurisdiccional (
    id integer NOT NULL,
    numero_anio character varying(50) NOT NULL,
    tipo_normativa_postitulo_jurisdiccional_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL,
    otorgada_por_id integer NOT NULL,
    observaciones character varying(255),
    estado_id integer NOT NULL,
    revisado_jurisdiccion boolean
);


--
-- TOC entry 556 (class 1259 OID 191370)
-- Dependencies: 6
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa_postitulo_jurisdiccional_estados (
    id integer NOT NULL,
    normativa_postitulo_jurisdiccional_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 555 (class 1259 OID 191368)
-- Dependencies: 556 6
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_postitulo_jurisdiccional_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3330 (class 0 OID 0)
-- Dependencies: 555
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_postitulo_jurisdiccional_estados_id_seq OWNED BY postitulos_normativa_postitulo_jurisdiccional_estados.id;


--
-- TOC entry 553 (class 1259 OID 191340)
-- Dependencies: 554 6
-- Name: postitulos_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3331 (class 0 OID 0)
-- Dependencies: 553
-- Name: postitulos_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_postitulo_jurisdiccional_id_seq OWNED BY postitulos_normativa_postitulo_jurisdiccional.id;


--
-- TOC entry 546 (class 1259 OID 191294)
-- Dependencies: 6
-- Name: postitulos_normativa_postitulos_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_normativa_postitulos_estados (
    id integer NOT NULL,
    normativa_postitulo_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 545 (class 1259 OID 191292)
-- Dependencies: 546 6
-- Name: postitulos_normativa_postitulos_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_normativa_postitulos_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3332 (class 0 OID 0)
-- Dependencies: 545
-- Name: postitulos_normativa_postitulos_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_normativa_postitulos_estados_id_seq OWNED BY postitulos_normativa_postitulos_estados.id;


--
-- TOC entry 522 (class 1259 OID 191063)
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
-- TOC entry 538 (class 1259 OID 191215)
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
-- TOC entry 537 (class 1259 OID 191213)
-- Dependencies: 538 6
-- Name: postitulos_postitulo_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3333 (class 0 OID 0)
-- Dependencies: 537
-- Name: postitulos_postitulo_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_estados_id_seq OWNED BY postitulos_postitulo_estados.id;


--
-- TOC entry 521 (class 1259 OID 191061)
-- Dependencies: 522 6
-- Name: postitulos_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3334 (class 0 OID 0)
-- Dependencies: 521
-- Name: postitulos_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_id_seq OWNED BY postitulos_postitulo.id;


--
-- TOC entry 542 (class 1259 OID 191248)
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
-- TOC entry 544 (class 1259 OID 191276)
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
-- TOC entry 543 (class 1259 OID 191274)
-- Dependencies: 544 6
-- Name: postitulos_postitulo_nacional_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_nacional_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3335 (class 0 OID 0)
-- Dependencies: 543
-- Name: postitulos_postitulo_nacional_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_nacional_estados_id_seq OWNED BY postitulos_postitulo_nacional_estados.id;


--
-- TOC entry 541 (class 1259 OID 191246)
-- Dependencies: 542 6
-- Name: postitulos_postitulo_nacional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulo_nacional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3336 (class 0 OID 0)
-- Dependencies: 541
-- Name: postitulos_postitulo_nacional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulo_nacional_id_seq OWNED BY postitulos_postitulo_nacional.id;


--
-- TOC entry 520 (class 1259 OID 191048)
-- Dependencies: 6
-- Name: postitulos_postitulos_areas; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_areas (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    areapostitulo_id integer NOT NULL
);


--
-- TOC entry 519 (class 1259 OID 191046)
-- Dependencies: 520 6
-- Name: postitulos_postitulos_areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_areas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3337 (class 0 OID 0)
-- Dependencies: 519
-- Name: postitulos_postitulos_areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_areas_id_seq OWNED BY postitulos_postitulos_areas.id;


--
-- TOC entry 516 (class 1259 OID 191018)
-- Dependencies: 6
-- Name: postitulos_postitulos_jurisdicciones; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_jurisdicciones (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    jurisdiccion_id integer NOT NULL
);


--
-- TOC entry 515 (class 1259 OID 191016)
-- Dependencies: 516 6
-- Name: postitulos_postitulos_jurisdicciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_jurisdicciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3338 (class 0 OID 0)
-- Dependencies: 515
-- Name: postitulos_postitulos_jurisdicciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_jurisdicciones_id_seq OWNED BY postitulos_postitulos_jurisdicciones.id;


--
-- TOC entry 540 (class 1259 OID 191233)
-- Dependencies: 6
-- Name: postitulos_postitulos_nacionales_carreras; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_nacionales_carreras (
    id integer NOT NULL,
    postitulonacional_id integer NOT NULL,
    carrerapostitulo_id integer NOT NULL
);


--
-- TOC entry 539 (class 1259 OID 191231)
-- Dependencies: 540 6
-- Name: postitulos_postitulos_nacionales_carreras_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_nacionales_carreras_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3339 (class 0 OID 0)
-- Dependencies: 539
-- Name: postitulos_postitulos_nacionales_carreras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_nacionales_carreras_id_seq OWNED BY postitulos_postitulos_nacionales_carreras.id;


--
-- TOC entry 518 (class 1259 OID 191033)
-- Dependencies: 6
-- Name: postitulos_postitulos_niveles; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_postitulos_niveles (
    id integer NOT NULL,
    postitulo_id integer NOT NULL,
    nivel_id integer NOT NULL
);


--
-- TOC entry 517 (class 1259 OID 191031)
-- Dependencies: 518 6
-- Name: postitulos_postitulos_niveles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_postitulos_niveles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3340 (class 0 OID 0)
-- Dependencies: 517
-- Name: postitulos_postitulos_niveles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_postitulos_niveles_id_seq OWNED BY postitulos_postitulos_niveles.id;


--
-- TOC entry 562 (class 1259 OID 191413)
-- Dependencies: 2912 2913 6
-- Name: postitulos_solicitud; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_solicitud (
    id integer NOT NULL,
    jurisdiccion_id integer NOT NULL,
    carrera_postitulo_id integer NOT NULL,
    postitulo_nacional_id integer NOT NULL,
    primera_cohorte integer,
    ultima_cohorte integer,
    nro_expediente character varying(200),
    normativas_postitulo character varying(99),
    estado_id integer NOT NULL,
    CONSTRAINT postitulos_solicitud_primera_cohorte_check CHECK ((primera_cohorte >= 0)),
    CONSTRAINT postitulos_solicitud_ultima_cohorte_check CHECK ((ultima_cohorte >= 0))
);


--
-- TOC entry 568 (class 1259 OID 191485)
-- Dependencies: 6
-- Name: postitulos_solicitud_anexos; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_solicitud_anexos (
    id integer NOT NULL,
    anexo_id integer NOT NULL,
    solicitud_id integer NOT NULL
);


--
-- TOC entry 567 (class 1259 OID 191483)
-- Dependencies: 568 6
-- Name: postitulos_solicitud_anexos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_solicitud_anexos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3341 (class 0 OID 0)
-- Dependencies: 567
-- Name: postitulos_solicitud_anexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_solicitud_anexos_id_seq OWNED BY postitulos_solicitud_anexos.id;


--
-- TOC entry 566 (class 1259 OID 191465)
-- Dependencies: 6
-- Name: postitulos_solicitud_establecimientos; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_solicitud_establecimientos (
    id integer NOT NULL,
    establecimiento_id integer NOT NULL,
    solicitud_id integer NOT NULL
);


--
-- TOC entry 565 (class 1259 OID 191463)
-- Dependencies: 566 6
-- Name: postitulos_solicitud_establecimientos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_solicitud_establecimientos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3342 (class 0 OID 0)
-- Dependencies: 565
-- Name: postitulos_solicitud_establecimientos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_solicitud_establecimientos_id_seq OWNED BY postitulos_solicitud_establecimientos.id;


--
-- TOC entry 584 (class 1259 OID 191629)
-- Dependencies: 6
-- Name: postitulos_solicitud_estados; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_solicitud_estados (
    id integer NOT NULL,
    solicitud_id integer NOT NULL,
    estado_id integer NOT NULL,
    fecha date NOT NULL
);


--
-- TOC entry 583 (class 1259 OID 191627)
-- Dependencies: 584 6
-- Name: postitulos_solicitud_estados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_solicitud_estados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3343 (class 0 OID 0)
-- Dependencies: 583
-- Name: postitulos_solicitud_estados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_solicitud_estados_id_seq OWNED BY postitulos_solicitud_estados.id;


--
-- TOC entry 561 (class 1259 OID 191411)
-- Dependencies: 562 6
-- Name: postitulos_solicitud_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_solicitud_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3344 (class 0 OID 0)
-- Dependencies: 561
-- Name: postitulos_solicitud_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_solicitud_id_seq OWNED BY postitulos_solicitud.id;


--
-- TOC entry 560 (class 1259 OID 191398)
-- Dependencies: 6
-- Name: postitulos_solicitud_normativas_jurisdiccionales; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_solicitud_normativas_jurisdiccionales (
    id integer NOT NULL,
    solicitud_id integer NOT NULL,
    normativapostitulojurisdiccional_id integer NOT NULL
);


--
-- TOC entry 559 (class 1259 OID 191396)
-- Dependencies: 560 6
-- Name: postitulos_solicitud_normativas_jurisdiccionales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_solicitud_normativas_jurisdiccionales_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3345 (class 0 OID 0)
-- Dependencies: 559
-- Name: postitulos_solicitud_normativas_jurisdiccionales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_solicitud_normativas_jurisdiccionales_id_seq OWNED BY postitulos_solicitud_normativas_jurisdiccionales.id;


--
-- TOC entry 514 (class 1259 OID 191008)
-- Dependencies: 6
-- Name: postitulos_tipo_normativa; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_tipo_normativa (
    id integer NOT NULL,
    descripcion character varying(50) NOT NULL
);


--
-- TOC entry 513 (class 1259 OID 191006)
-- Dependencies: 514 6
-- Name: postitulos_tipo_normativa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_tipo_normativa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3346 (class 0 OID 0)
-- Dependencies: 513
-- Name: postitulos_tipo_normativa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_tipo_normativa_id_seq OWNED BY postitulos_tipo_normativa.id;


--
-- TOC entry 548 (class 1259 OID 191312)
-- Dependencies: 6
-- Name: postitulos_tipo_normativa_postitulo_jurisdiccional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_tipo_normativa_postitulo_jurisdiccional (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 547 (class 1259 OID 191310)
-- Dependencies: 548 6
-- Name: postitulos_tipo_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_tipo_normativa_postitulo_jurisdiccional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3347 (class 0 OID 0)
-- Dependencies: 547
-- Name: postitulos_tipo_normativa_postitulo_jurisdiccional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_tipo_normativa_postitulo_jurisdiccional_id_seq OWNED BY postitulos_tipo_normativa_postitulo_jurisdiccional.id;


--
-- TOC entry 512 (class 1259 OID 190998)
-- Dependencies: 6
-- Name: postitulos_tipo_postitulo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_tipo_postitulo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


--
-- TOC entry 511 (class 1259 OID 190996)
-- Dependencies: 512 6
-- Name: postitulos_tipo_postitulo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_tipo_postitulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3348 (class 0 OID 0)
-- Dependencies: 511
-- Name: postitulos_tipo_postitulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_tipo_postitulo_id_seq OWNED BY postitulos_tipo_postitulo.id;


--
-- TOC entry 564 (class 1259 OID 191448)
-- Dependencies: 2915 6
-- Name: postitulos_validez_nacional; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE postitulos_validez_nacional (
    id integer NOT NULL,
    solicitud_id integer NOT NULL,
    nro_infd character varying(99) NOT NULL,
    cue character varying(9) NOT NULL,
    tipo_unidad_educativa character varying(10) NOT NULL,
    unidad_educativa_id integer NOT NULL,
    carrera_postitulo character varying(255),
    postitulo_nacional character varying(255),
    primera_cohorte character varying(255),
    ultima_cohorte character varying(255),
    normativas_postitulo character varying(255),
    normativa_postitulo_jurisdiccional character varying(255),
    referencia character varying(10),
    CONSTRAINT postitulos_validez_nacional_unidad_educativa_id_check CHECK ((unidad_educativa_id >= 0))
);


--
-- TOC entry 563 (class 1259 OID 191446)
-- Dependencies: 564 6
-- Name: postitulos_validez_nacional_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE postitulos_validez_nacional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3349 (class 0 OID 0)
-- Dependencies: 563
-- Name: postitulos_validez_nacional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE postitulos_validez_nacional_id_seq OWNED BY postitulos_validez_nacional.id;


--
-- TOC entry 2880 (class 2604 OID 190917)
-- Dependencies: 499 500 500
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_area_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_area_postitulo_id_seq'::regclass);


--
-- TOC entry 2884 (class 2604 OID 190973)
-- Dependencies: 507 508 508
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_estados_id_seq'::regclass);


--
-- TOC entry 2896 (class 2604 OID 191160)
-- Dependencies: 531 532 532
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2897 (class 2604 OID 191190)
-- Dependencies: 533 534 534
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_carrera_postitulo_jurisdiccional_estados_id_seq'::regclass);


--
-- TOC entry 2883 (class 2604 OID 190952)
-- Dependencies: 505 506 506
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrerapostitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_carrerapostitulo_id_seq'::regclass);


--
-- TOC entry 2882 (class 2604 OID 190937)
-- Dependencies: 503 504 504
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones ALTER COLUMN id SET DEFAULT nextval('postitulos_carreras_postitulo_jurisdicciones_id_seq'::regclass);


--
-- TOC entry 2895 (class 2604 OID 191145)
-- Dependencies: 529 530 530
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas ALTER COLUMN id SET DEFAULT nextval('postitulos_carreras_postitulos_normativas_id_seq'::regclass);


--
-- TOC entry 2918 (class 2604 OID 191508)
-- Dependencies: 569 570 570
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohorte_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_cohorte_postitulo_id_seq'::regclass);


--
-- TOC entry 2924 (class 2604 OID 191570)
-- Dependencies: 577 578 578
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos ALTER COLUMN id SET DEFAULT nextval('postitulos_cohortes_postitulo_anexos_id_seq'::regclass);


--
-- TOC entry 2921 (class 2604 OID 191534)
-- Dependencies: 573 574 574
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos ALTER COLUMN id SET DEFAULT nextval('postitulos_cohortes_postitulo_establecimientos_id_seq'::regclass);


--
-- TOC entry 2927 (class 2604 OID 191606)
-- Dependencies: 581 582 582
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas ALTER COLUMN id SET DEFAULT nextval('postitulos_cohortes_postitulo_extensiones_aulicas_id_seq'::regclass);


--
-- TOC entry 2881 (class 2604 OID 190927)
-- Dependencies: 501 502 502
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_carrera_postitulo_id_seq'::regclass);


--
-- TOC entry 2892 (class 2604 OID 191107)
-- Dependencies: 523 524 524
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_carrera_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2923 (class 2604 OID 191560)
-- Dependencies: 575 576 576
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_anexo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_cohorte_postitulo_anexo_id_seq'::regclass);


--
-- TOC entry 2920 (class 2604 OID 191524)
-- Dependencies: 571 572 572
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_establecimiento ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_cohorte_postitulo_establecimiento_id_seq'::regclass);


--
-- TOC entry 2926 (class 2604 OID 191596)
-- Dependencies: 579 580 580
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_extension_aulica ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_cohorte_postitulo_extension_aulica_id_seq'::regclass);


--
-- TOC entry 2893 (class 2604 OID 191117)
-- Dependencies: 525 526 526
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_normativa_postitulo_id_seq'::regclass);


--
-- TOC entry 2906 (class 2604 OID 191335)
-- Dependencies: 551 552 552
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_normativa_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2885 (class 2604 OID 190991)
-- Dependencies: 509 510 510
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_postitulo_id_seq'::regclass);


--
-- TOC entry 2898 (class 2604 OID 191208)
-- Dependencies: 535 536 536
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_postitulo_nacional_id_seq'::regclass);


--
-- TOC entry 2909 (class 2604 OID 191391)
-- Dependencies: 557 558 558
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_estado_solicitud ALTER COLUMN id SET DEFAULT nextval('postitulos_estado_solicitud_id_seq'::regclass);


--
-- TOC entry 2894 (class 2604 OID 191127)
-- Dependencies: 527 528 528
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_id_seq'::regclass);


--
-- TOC entry 2905 (class 2604 OID 191325)
-- Dependencies: 549 550 550
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_motivo_otorgamiento ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_motivo_otorgamiento_id_seq'::regclass);


--
-- TOC entry 2907 (class 2604 OID 191345)
-- Dependencies: 553 554 554
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2908 (class 2604 OID 191373)
-- Dependencies: 555 556 556
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_postitulo_jurisdiccional_estados_id_seq'::regclass);


--
-- TOC entry 2903 (class 2604 OID 191297)
-- Dependencies: 545 546 546
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_normativa_postitulos_estados_id_seq'::regclass);


--
-- TOC entry 2891 (class 2604 OID 191066)
-- Dependencies: 521 522 522
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_id_seq'::regclass);


--
-- TOC entry 2899 (class 2604 OID 191218)
-- Dependencies: 537 538 538
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_estados_id_seq'::regclass);


--
-- TOC entry 2901 (class 2604 OID 191251)
-- Dependencies: 541 542 542
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_nacional_id_seq'::regclass);


--
-- TOC entry 2902 (class 2604 OID 191279)
-- Dependencies: 543 544 544
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulo_nacional_estados_id_seq'::regclass);


--
-- TOC entry 2890 (class 2604 OID 191051)
-- Dependencies: 519 520 520
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_areas_id_seq'::regclass);


--
-- TOC entry 2888 (class 2604 OID 191021)
-- Dependencies: 515 516 516
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_jurisdicciones_id_seq'::regclass);


--
-- TOC entry 2900 (class 2604 OID 191236)
-- Dependencies: 539 540 540
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_nacionales_carreras_id_seq'::regclass);


--
-- TOC entry 2889 (class 2604 OID 191036)
-- Dependencies: 517 518 518
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles ALTER COLUMN id SET DEFAULT nextval('postitulos_postitulos_niveles_id_seq'::regclass);


--
-- TOC entry 2911 (class 2604 OID 191416)
-- Dependencies: 561 562 562
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud ALTER COLUMN id SET DEFAULT nextval('postitulos_solicitud_id_seq'::regclass);


--
-- TOC entry 2917 (class 2604 OID 191488)
-- Dependencies: 567 568 568
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_anexos ALTER COLUMN id SET DEFAULT nextval('postitulos_solicitud_anexos_id_seq'::regclass);


--
-- TOC entry 2916 (class 2604 OID 191468)
-- Dependencies: 565 566 566
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_establecimientos ALTER COLUMN id SET DEFAULT nextval('postitulos_solicitud_establecimientos_id_seq'::regclass);


--
-- TOC entry 2929 (class 2604 OID 191632)
-- Dependencies: 583 584 584
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_estados ALTER COLUMN id SET DEFAULT nextval('postitulos_solicitud_estados_id_seq'::regclass);


--
-- TOC entry 2910 (class 2604 OID 191401)
-- Dependencies: 559 560 560
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_normativas_jurisdiccionales ALTER COLUMN id SET DEFAULT nextval('postitulos_solicitud_normativas_jurisdiccionales_id_seq'::regclass);


--
-- TOC entry 2887 (class 2604 OID 191011)
-- Dependencies: 513 514 514
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_tipo_normativa ALTER COLUMN id SET DEFAULT nextval('postitulos_tipo_normativa_id_seq'::regclass);


--
-- TOC entry 2904 (class 2604 OID 191315)
-- Dependencies: 547 548 548
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_tipo_normativa_postitulo_jurisdiccional ALTER COLUMN id SET DEFAULT nextval('postitulos_tipo_normativa_postitulo_jurisdiccional_id_seq'::regclass);


--
-- TOC entry 2886 (class 2604 OID 191001)
-- Dependencies: 511 512 512
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_tipo_postitulo ALTER COLUMN id SET DEFAULT nextval('postitulos_tipo_postitulo_id_seq'::regclass);


--
-- TOC entry 2914 (class 2604 OID 191451)
-- Dependencies: 563 564 564
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_validez_nacional ALTER COLUMN id SET DEFAULT nextval('postitulos_validez_nacional_id_seq'::regclass);


--
-- TOC entry 2931 (class 2606 OID 190921)
-- Dependencies: 500 500 3304
-- Name: postitulos_area_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_area_postitulo
    ADD CONSTRAINT postitulos_area_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2933 (class 2606 OID 190919)
-- Dependencies: 500 500 3304
-- Name: postitulos_area_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_area_postitulo
    ADD CONSTRAINT postitulos_area_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3006 (class 2606 OID 191164)
-- Dependencies: 532 532 532 3304
-- Name: postitulos_carrera_postitulo__carrera_postitulo_id_jurisdic_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo__carrera_postitulo_id_jurisdic_key UNIQUE (carrera_postitulo_id, jurisdiccion_id);


--
-- TOC entry 2950 (class 2606 OID 190975)
-- Dependencies: 508 508 3304
-- Name: postitulos_carrera_postitulo_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3015 (class 2606 OID 191192)
-- Dependencies: 534 534 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3011 (class 2606 OID 191162)
-- Dependencies: 532 532 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2946 (class 2606 OID 190957)
-- Dependencies: 506 506 3304
-- Name: postitulos_carrerapostitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carrerapostitulo
    ADD CONSTRAINT postitulos_carrerapostitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2939 (class 2606 OID 190941)
-- Dependencies: 504 504 504 3304
-- Name: postitulos_carreras_postitulo_carrerapostitulo_id_jurisdicc_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_carrerapostitulo_id_jurisdicc_key UNIQUE (carrerapostitulo_id, jurisdiccion_id);


--
-- TOC entry 3000 (class 2606 OID 191149)
-- Dependencies: 530 530 530 3304
-- Name: postitulos_carreras_postitulo_carrerapostitulojurisdicciona_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulo_carrerapostitulojurisdicciona_key UNIQUE (carrerapostitulojurisdiccional_id, normativapostitulo_id);


--
-- TOC entry 2943 (class 2606 OID 190939)
-- Dependencies: 504 504 3304
-- Name: postitulos_carreras_postitulo_jurisdicciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_jurisdicciones_pkey PRIMARY KEY (id);


--
-- TOC entry 3004 (class 2606 OID 191147)
-- Dependencies: 530 530 3304
-- Name: postitulos_carreras_postitulos_normativas_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulos_normativas_pkey PRIMARY KEY (id);


--
-- TOC entry 3100 (class 2606 OID 191513)
-- Dependencies: 570 570 570 3304
-- Name: postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccion_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohorte_postitulo
    ADD CONSTRAINT postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccion_key UNIQUE (carrera_postitulo_jurisdiccional_id, anio);


--
-- TOC entry 3103 (class 2606 OID 191511)
-- Dependencies: 570 570 3304
-- Name: postitulos_cohorte_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohorte_postitulo
    ADD CONSTRAINT postitulos_cohorte_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3120 (class 2606 OID 191575)
-- Dependencies: 578 578 578 3304
-- Name: postitulos_cohortes_postitulo_anexo_id_cohorte_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos
    ADD CONSTRAINT postitulos_cohortes_postitulo_anexo_id_cohorte_postitulo_id_key UNIQUE (anexo_id, cohorte_postitulo_id);


--
-- TOC entry 3125 (class 2606 OID 191573)
-- Dependencies: 578 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos
    ADD CONSTRAINT postitulos_cohortes_postitulo_anexos_pkey PRIMARY KEY (id);


--
-- TOC entry 3109 (class 2606 OID 191539)
-- Dependencies: 574 574 574 3304
-- Name: postitulos_cohortes_postitulo_establecimiento_id_cohorte_po_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos
    ADD CONSTRAINT postitulos_cohortes_postitulo_establecimiento_id_cohorte_po_key UNIQUE (establecimiento_id, cohorte_postitulo_id);


--
-- TOC entry 3114 (class 2606 OID 191537)
-- Dependencies: 574 574 3304
-- Name: postitulos_cohortes_postitulo_establecimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos
    ADD CONSTRAINT postitulos_cohortes_postitulo_establecimientos_pkey PRIMARY KEY (id);


--
-- TOC entry 3131 (class 2606 OID 191611)
-- Dependencies: 582 582 582 3304
-- Name: postitulos_cohortes_postitulo_extension_aulica_id_cohorte_p_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas
    ADD CONSTRAINT postitulos_cohortes_postitulo_extension_aulica_id_cohorte_p_key UNIQUE (extension_aulica_id, cohorte_postitulo_id);


--
-- TOC entry 3136 (class 2606 OID 191609)
-- Dependencies: 582 582 3304
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas
    ADD CONSTRAINT postitulos_cohortes_postitulo_extensiones_aulicas_pkey PRIMARY KEY (id);


--
-- TOC entry 2987 (class 2606 OID 191111)
-- Dependencies: 524 524 3304
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_jurisdiccional_nombre_key UNIQUE (nombre);


--
-- TOC entry 2989 (class 2606 OID 191109)
-- Dependencies: 524 524 3304
-- Name: postitulos_estado_carrera_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2935 (class 2606 OID 190931)
-- Dependencies: 502 502 3304
-- Name: postitulos_estado_carrera_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2937 (class 2606 OID 190929)
-- Dependencies: 502 502 3304
-- Name: postitulos_estado_carrera_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_carrera_postitulo
    ADD CONSTRAINT postitulos_estado_carrera_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3116 (class 2606 OID 191564)
-- Dependencies: 576 576 3304
-- Name: postitulos_estado_cohorte_postitulo_anexo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_anexo
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_anexo_nombre_key UNIQUE (nombre);


--
-- TOC entry 3118 (class 2606 OID 191562)
-- Dependencies: 576 576 3304
-- Name: postitulos_estado_cohorte_postitulo_anexo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_anexo
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_anexo_pkey PRIMARY KEY (id);


--
-- TOC entry 3105 (class 2606 OID 191528)
-- Dependencies: 572 572 3304
-- Name: postitulos_estado_cohorte_postitulo_establecimiento_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_establecimiento
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_establecimiento_nombre_key UNIQUE (nombre);


--
-- TOC entry 3107 (class 2606 OID 191526)
-- Dependencies: 572 572 3304
-- Name: postitulos_estado_cohorte_postitulo_establecimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_establecimiento
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_establecimiento_pkey PRIMARY KEY (id);


--
-- TOC entry 3127 (class 2606 OID 191600)
-- Dependencies: 580 580 3304
-- Name: postitulos_estado_cohorte_postitulo_extension_aulica_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_extension_aulica
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_extension_aulica_nombre_key UNIQUE (nombre);


--
-- TOC entry 3129 (class 2606 OID 191598)
-- Dependencies: 580 580 3304
-- Name: postitulos_estado_cohorte_postitulo_extension_aulica_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_cohorte_postitulo_extension_aulica
    ADD CONSTRAINT postitulos_estado_cohorte_postitulo_extension_aulica_pkey PRIMARY KEY (id);


--
-- TOC entry 3053 (class 2606 OID 191339)
-- Dependencies: 552 552 3304
-- Name: postitulos_estado_normativa_postitulo_jurisdiccional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_normativa_postitulo_jurisdiccional_nombre_key UNIQUE (nombre);


--
-- TOC entry 3055 (class 2606 OID 191337)
-- Dependencies: 552 552 3304
-- Name: postitulos_estado_normativa_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_estado_normativa_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2991 (class 2606 OID 191121)
-- Dependencies: 526 526 3304
-- Name: postitulos_estado_normativa_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo
    ADD CONSTRAINT postitulos_estado_normativa_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2993 (class 2606 OID 191119)
-- Dependencies: 526 526 3304
-- Name: postitulos_estado_normativa_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_normativa_postitulo
    ADD CONSTRAINT postitulos_estado_normativa_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3017 (class 2606 OID 191212)
-- Dependencies: 536 536 3304
-- Name: postitulos_estado_postitulo_nacional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional
    ADD CONSTRAINT postitulos_estado_postitulo_nacional_nombre_key UNIQUE (nombre);


--
-- TOC entry 3019 (class 2606 OID 191210)
-- Dependencies: 536 536 3304
-- Name: postitulos_estado_postitulo_nacional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo_nacional
    ADD CONSTRAINT postitulos_estado_postitulo_nacional_pkey PRIMARY KEY (id);


--
-- TOC entry 2952 (class 2606 OID 190995)
-- Dependencies: 510 510 3304
-- Name: postitulos_estado_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo
    ADD CONSTRAINT postitulos_estado_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2954 (class 2606 OID 190993)
-- Dependencies: 510 510 3304
-- Name: postitulos_estado_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_postitulo
    ADD CONSTRAINT postitulos_estado_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3067 (class 2606 OID 191395)
-- Dependencies: 558 558 3304
-- Name: postitulos_estado_solicitud_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_solicitud
    ADD CONSTRAINT postitulos_estado_solicitud_nombre_key UNIQUE (nombre);


--
-- TOC entry 3069 (class 2606 OID 191393)
-- Dependencies: 558 558 3304
-- Name: postitulos_estado_solicitud_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_estado_solicitud
    ADD CONSTRAINT postitulos_estado_solicitud_pkey PRIMARY KEY (id);


--
-- TOC entry 3049 (class 2606 OID 191329)
-- Dependencies: 550 550 3304
-- Name: postitulos_normativa_motivo_otorgamiento_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_motivo_otorgamiento
    ADD CONSTRAINT postitulos_normativa_motivo_otorgamiento_nombre_key UNIQUE (nombre);


--
-- TOC entry 3051 (class 2606 OID 191327)
-- Dependencies: 550 550 3304
-- Name: postitulos_normativa_motivo_otorgamiento_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_motivo_otorgamiento
    ADD CONSTRAINT postitulos_normativa_motivo_otorgamiento_pkey PRIMARY KEY (id);


--
-- TOC entry 2996 (class 2606 OID 191134)
-- Dependencies: 528 528 3304
-- Name: postitulos_normativa_numero_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_numero_key UNIQUE (numero);


--
-- TOC entry 2998 (class 2606 OID 191132)
-- Dependencies: 528 528 3304
-- Name: postitulos_normativa_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_pkey PRIMARY KEY (id);


--
-- TOC entry 3065 (class 2606 OID 191375)
-- Dependencies: 556 556 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccional_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3060 (class 2606 OID 191347)
-- Dependencies: 554 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 3043 (class 2606 OID 191299)
-- Dependencies: 546 546 3304
-- Name: postitulos_normativa_postitulos_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3022 (class 2606 OID 191220)
-- Dependencies: 538 538 3304
-- Name: postitulos_postitulo_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3038 (class 2606 OID 191281)
-- Dependencies: 544 544 3304
-- Name: postitulos_postitulo_nacional_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3032 (class 2606 OID 191258)
-- Dependencies: 542 542 542 3304
-- Name: postitulos_postitulo_nacional_nombre_normativa_postitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_nombre_normativa_postitulo_id_key UNIQUE (nombre, normativa_postitulo_id);


--
-- TOC entry 3035 (class 2606 OID 191256)
-- Dependencies: 542 542 3304
-- Name: postitulos_postitulo_nacional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_pkey PRIMARY KEY (id);


--
-- TOC entry 2984 (class 2606 OID 191071)
-- Dependencies: 522 522 3304
-- Name: postitulos_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 2977 (class 2606 OID 191053)
-- Dependencies: 520 520 3304
-- Name: postitulos_postitulos_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_pkey PRIMARY KEY (id);


--
-- TOC entry 2980 (class 2606 OID 191055)
-- Dependencies: 520 520 520 3304
-- Name: postitulos_postitulos_areas_postitulo_id_areapostitulo_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_postitulo_id_areapostitulo_id_key UNIQUE (postitulo_id, areapostitulo_id);


--
-- TOC entry 2964 (class 2606 OID 191025)
-- Dependencies: 516 516 516 3304
-- Name: postitulos_postitulos_jurisdic_postitulo_id_jurisdiccion_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdic_postitulo_id_jurisdiccion_id_key UNIQUE (postitulo_id, jurisdiccion_id);


--
-- TOC entry 2967 (class 2606 OID 191023)
-- Dependencies: 516 516 3304
-- Name: postitulos_postitulos_jurisdicciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdicciones_pkey PRIMARY KEY (id);


--
-- TOC entry 3025 (class 2606 OID 191240)
-- Dependencies: 540 540 540 3304
-- Name: postitulos_postitulos_naciona_postitulonacional_id_carrerap_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_naciona_postitulonacional_id_carrerap_key UNIQUE (postitulonacional_id, carrerapostitulo_id);


--
-- TOC entry 3028 (class 2606 OID 191238)
-- Dependencies: 540 540 3304
-- Name: postitulos_postitulos_nacionales_carreras_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_nacionales_carreras_pkey PRIMARY KEY (id);


--
-- TOC entry 2971 (class 2606 OID 191038)
-- Dependencies: 518 518 3304
-- Name: postitulos_postitulos_niveles_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_pkey PRIMARY KEY (id);


--
-- TOC entry 2974 (class 2606 OID 191040)
-- Dependencies: 518 518 518 3304
-- Name: postitulos_postitulos_niveles_postitulo_id_nivel_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_postitulo_id_nivel_id_key UNIQUE (postitulo_id, nivel_id);


--
-- TOC entry 3095 (class 2606 OID 191492)
-- Dependencies: 568 568 568 3304
-- Name: postitulos_solicitud_anexos_anexo_id_solicitud_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_anexos
    ADD CONSTRAINT postitulos_solicitud_anexos_anexo_id_solicitud_id_key UNIQUE (anexo_id, solicitud_id);


--
-- TOC entry 3097 (class 2606 OID 191490)
-- Dependencies: 568 568 3304
-- Name: postitulos_solicitud_anexos_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_anexos
    ADD CONSTRAINT postitulos_solicitud_anexos_pkey PRIMARY KEY (id);


--
-- TOC entry 3088 (class 2606 OID 191472)
-- Dependencies: 566 566 566 3304
-- Name: postitulos_solicitud_establec_establecimiento_id_solicitud__key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_establecimientos
    ADD CONSTRAINT postitulos_solicitud_establec_establecimiento_id_solicitud__key UNIQUE (establecimiento_id, solicitud_id);


--
-- TOC entry 3091 (class 2606 OID 191470)
-- Dependencies: 566 566 3304
-- Name: postitulos_solicitud_establecimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_establecimientos
    ADD CONSTRAINT postitulos_solicitud_establecimientos_pkey PRIMARY KEY (id);


--
-- TOC entry 3139 (class 2606 OID 191634)
-- Dependencies: 584 584 3304
-- Name: postitulos_solicitud_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_estados
    ADD CONSTRAINT postitulos_solicitud_estados_pkey PRIMARY KEY (id);


--
-- TOC entry 3071 (class 2606 OID 191405)
-- Dependencies: 560 560 560 3304
-- Name: postitulos_solicitud_normativ_solicitud_id_normativapostitu_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_normativas_jurisdiccionales
    ADD CONSTRAINT postitulos_solicitud_normativ_solicitud_id_normativapostitu_key UNIQUE (solicitud_id, normativapostitulojurisdiccional_id);


--
-- TOC entry 3074 (class 2606 OID 191403)
-- Dependencies: 560 560 3304
-- Name: postitulos_solicitud_normativas_jurisdiccionales_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud_normativas_jurisdiccionales
    ADD CONSTRAINT postitulos_solicitud_normativas_jurisdiccionales_pkey PRIMARY KEY (id);


--
-- TOC entry 3080 (class 2606 OID 191420)
-- Dependencies: 562 562 3304
-- Name: postitulos_solicitud_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_solicitud
    ADD CONSTRAINT postitulos_solicitud_pkey PRIMARY KEY (id);


--
-- TOC entry 2960 (class 2606 OID 191015)
-- Dependencies: 514 514 3304
-- Name: postitulos_tipo_normativa_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa
    ADD CONSTRAINT postitulos_tipo_normativa_descripcion_key UNIQUE (descripcion);


--
-- TOC entry 2962 (class 2606 OID 191013)
-- Dependencies: 514 514 3304
-- Name: postitulos_tipo_normativa_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa
    ADD CONSTRAINT postitulos_tipo_normativa_pkey PRIMARY KEY (id);


--
-- TOC entry 3045 (class 2606 OID 191319)
-- Dependencies: 548 548 3304
-- Name: postitulos_tipo_normativa_postitulo_jurisdiccional_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_tipo_normativa_postitulo_jurisdiccional_nombre_key UNIQUE (nombre);


--
-- TOC entry 3047 (class 2606 OID 191317)
-- Dependencies: 548 548 3304
-- Name: postitulos_tipo_normativa_postitulo_jurisdiccional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_tipo_normativa_postitulo_jurisdiccional_pkey PRIMARY KEY (id);


--
-- TOC entry 2956 (class 2606 OID 191005)
-- Dependencies: 512 512 3304
-- Name: postitulos_tipo_postitulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_postitulo
    ADD CONSTRAINT postitulos_tipo_postitulo_nombre_key UNIQUE (nombre);


--
-- TOC entry 2958 (class 2606 OID 191003)
-- Dependencies: 512 512 3304
-- Name: postitulos_tipo_postitulo_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_tipo_postitulo
    ADD CONSTRAINT postitulos_tipo_postitulo_pkey PRIMARY KEY (id);


--
-- TOC entry 3085 (class 2606 OID 191457)
-- Dependencies: 564 564 3304
-- Name: postitulos_validez_nacional_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY postitulos_validez_nacional
    ADD CONSTRAINT postitulos_validez_nacional_pkey PRIMARY KEY (id);


--
-- TOC entry 2947 (class 1259 OID 191648)
-- Dependencies: 508 3304
-- Name: postitulos_carrera_postitulo_estados_carrera_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_estados_carrera_postitulo_id ON postitulos_carrera_postitulo_estados USING btree (carrera_postitulo_id);


--
-- TOC entry 2948 (class 1259 OID 191649)
-- Dependencies: 508 3304
-- Name: postitulos_carrera_postitulo_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_estados_estado_id ON postitulos_carrera_postitulo_estados USING btree (estado_id);


--
-- TOC entry 3007 (class 1259 OID 191662)
-- Dependencies: 532 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_carrera_postitulo_i; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_carrera_postitulo_i ON postitulos_carrera_postitulo_jurisdiccional USING btree (carrera_postitulo_id);


--
-- TOC entry 3008 (class 1259 OID 191664)
-- Dependencies: 532 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estado_id ON postitulos_carrera_postitulo_jurisdiccional USING btree (estado_id);


--
-- TOC entry 3012 (class 1259 OID 191665)
-- Dependencies: 534 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_carrera_pos; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estados_carrera_pos ON postitulos_carrera_postitulo_jurisdiccional_estados USING btree (carrera_postitulo_jurisdiccional_id);


--
-- TOC entry 3013 (class 1259 OID 191666)
-- Dependencies: 534 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_estados_estado_id ON postitulos_carrera_postitulo_jurisdiccional_estados USING btree (estado_id);


--
-- TOC entry 3009 (class 1259 OID 191663)
-- Dependencies: 532 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrera_postitulo_jurisdiccional_jurisdiccion_id ON postitulos_carrera_postitulo_jurisdiccional USING btree (jurisdiccion_id);


--
-- TOC entry 2944 (class 1259 OID 191647)
-- Dependencies: 506 3304
-- Name: postitulos_carrerapostitulo_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carrerapostitulo_estado_id ON postitulos_carrerapostitulo USING btree (estado_id);


--
-- TOC entry 2940 (class 1259 OID 191645)
-- Dependencies: 504 3304
-- Name: postitulos_carreras_postitulo_jurisdicciones_carrerapostitulo_i; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulo_jurisdicciones_carrerapostitulo_i ON postitulos_carreras_postitulo_jurisdicciones USING btree (carrerapostitulo_id);


--
-- TOC entry 2941 (class 1259 OID 191646)
-- Dependencies: 504 3304
-- Name: postitulos_carreras_postitulo_jurisdicciones_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulo_jurisdicciones_jurisdiccion_id ON postitulos_carreras_postitulo_jurisdicciones USING btree (jurisdiccion_id);


--
-- TOC entry 3001 (class 1259 OID 191660)
-- Dependencies: 530 3304
-- Name: postitulos_carreras_postitulos_normativas_carrerapostitulojuris; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulos_normativas_carrerapostitulojuris ON postitulos_carreras_postitulos_normativas USING btree (carrerapostitulojurisdiccional_id);


--
-- TOC entry 3002 (class 1259 OID 191661)
-- Dependencies: 530 3304
-- Name: postitulos_carreras_postitulos_normativas_normativapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_carreras_postitulos_normativas_normativapostitulo_id ON postitulos_carreras_postitulos_normativas USING btree (normativapostitulo_id);


--
-- TOC entry 3101 (class 1259 OID 191696)
-- Dependencies: 570 3304
-- Name: postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccional_i; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccional_i ON postitulos_cohorte_postitulo USING btree (carrera_postitulo_jurisdiccional_id);


--
-- TOC entry 3121 (class 1259 OID 191700)
-- Dependencies: 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_anexo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_anexos_anexo_id ON postitulos_cohortes_postitulo_anexos USING btree (anexo_id);


--
-- TOC entry 3122 (class 1259 OID 191701)
-- Dependencies: 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_cohorte_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_anexos_cohorte_postitulo_id ON postitulos_cohortes_postitulo_anexos USING btree (cohorte_postitulo_id);


--
-- TOC entry 3123 (class 1259 OID 191702)
-- Dependencies: 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_anexos_estado_id ON postitulos_cohortes_postitulo_anexos USING btree (estado_id);


--
-- TOC entry 3110 (class 1259 OID 191698)
-- Dependencies: 574 3304
-- Name: postitulos_cohortes_postitulo_establecimientos_cohorte_postitul; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_establecimientos_cohorte_postitul ON postitulos_cohortes_postitulo_establecimientos USING btree (cohorte_postitulo_id);


--
-- TOC entry 3111 (class 1259 OID 191697)
-- Dependencies: 574 3304
-- Name: postitulos_cohortes_postitulo_establecimientos_establecimiento_; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_establecimientos_establecimiento_ ON postitulos_cohortes_postitulo_establecimientos USING btree (establecimiento_id);


--
-- TOC entry 3112 (class 1259 OID 191699)
-- Dependencies: 574 3304
-- Name: postitulos_cohortes_postitulo_establecimientos_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_establecimientos_estado_id ON postitulos_cohortes_postitulo_establecimientos USING btree (estado_id);


--
-- TOC entry 3132 (class 1259 OID 191704)
-- Dependencies: 582 3304
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_cohorte_posti; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_extensiones_aulicas_cohorte_posti ON postitulos_cohortes_postitulo_extensiones_aulicas USING btree (cohorte_postitulo_id);


--
-- TOC entry 3133 (class 1259 OID 191705)
-- Dependencies: 582 3304
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_extensiones_aulicas_estado_id ON postitulos_cohortes_postitulo_extensiones_aulicas USING btree (estado_id);


--
-- TOC entry 3134 (class 1259 OID 191703)
-- Dependencies: 582 3304
-- Name: postitulos_cohortes_postitulo_extensiones_aulicas_extension_aul; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_cohortes_postitulo_extensiones_aulicas_extension_aul ON postitulos_cohortes_postitulo_extensiones_aulicas USING btree (extension_aulica_id);


--
-- TOC entry 2994 (class 1259 OID 191659)
-- Dependencies: 528 3304
-- Name: postitulos_normativa_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_estado_id ON postitulos_normativa USING btree (estado_id);


--
-- TOC entry 3056 (class 1259 OID 191680)
-- Dependencies: 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_estado_id ON postitulos_normativa_postitulo_jurisdiccional USING btree (estado_id);


--
-- TOC entry 3062 (class 1259 OID 191682)
-- Dependencies: 556 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_estados_estado_id ON postitulos_normativa_postitulo_jurisdiccional_estados USING btree (estado_id);


--
-- TOC entry 3063 (class 1259 OID 191681)
-- Dependencies: 556 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_estados_normativa; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_estados_normativa ON postitulos_normativa_postitulo_jurisdiccional_estados USING btree (normativa_postitulo_jurisdiccional_id);


--
-- TOC entry 3057 (class 1259 OID 191678)
-- Dependencies: 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_jurisdiccion_id ON postitulos_normativa_postitulo_jurisdiccional USING btree (jurisdiccion_id);


--
-- TOC entry 3058 (class 1259 OID 191679)
-- Dependencies: 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_otorgada_por_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_otorgada_por_id ON postitulos_normativa_postitulo_jurisdiccional USING btree (otorgada_por_id);


--
-- TOC entry 3061 (class 1259 OID 191677)
-- Dependencies: 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_tipo_normativa_po; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulo_jurisdiccional_tipo_normativa_po ON postitulos_normativa_postitulo_jurisdiccional USING btree (tipo_normativa_postitulo_jurisdiccional_id);


--
-- TOC entry 3040 (class 1259 OID 191676)
-- Dependencies: 546 3304
-- Name: postitulos_normativa_postitulos_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulos_estados_estado_id ON postitulos_normativa_postitulos_estados USING btree (estado_id);


--
-- TOC entry 3041 (class 1259 OID 191675)
-- Dependencies: 546 3304
-- Name: postitulos_normativa_postitulos_estados_normativa_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_normativa_postitulos_estados_normativa_postitulo_id ON postitulos_normativa_postitulos_estados USING btree (normativa_postitulo_id);


--
-- TOC entry 2981 (class 1259 OID 191657)
-- Dependencies: 522 3304
-- Name: postitulos_postitulo_carrera_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_carrera_postitulo_id ON postitulos_postitulo USING btree (carrera_postitulo_id);


--
-- TOC entry 2982 (class 1259 OID 191658)
-- Dependencies: 522 3304
-- Name: postitulos_postitulo_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estado_id ON postitulos_postitulo USING btree (estado_id);


--
-- TOC entry 3020 (class 1259 OID 191668)
-- Dependencies: 538 3304
-- Name: postitulos_postitulo_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estados_estado_id ON postitulos_postitulo_estados USING btree (estado_id);


--
-- TOC entry 3023 (class 1259 OID 191667)
-- Dependencies: 538 3304
-- Name: postitulos_postitulo_estados_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_estados_postitulo_id ON postitulos_postitulo_estados USING btree (postitulo_id);


--
-- TOC entry 3030 (class 1259 OID 191672)
-- Dependencies: 542 3304
-- Name: postitulos_postitulo_nacional_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estado_id ON postitulos_postitulo_nacional USING btree (estado_id);


--
-- TOC entry 3036 (class 1259 OID 191674)
-- Dependencies: 544 3304
-- Name: postitulos_postitulo_nacional_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estados_estado_id ON postitulos_postitulo_nacional_estados USING btree (estado_id);


--
-- TOC entry 3039 (class 1259 OID 191673)
-- Dependencies: 544 3304
-- Name: postitulos_postitulo_nacional_estados_postitulo_nacional_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_estados_postitulo_nacional_id ON postitulos_postitulo_nacional_estados USING btree (postitulo_nacional_id);


--
-- TOC entry 3033 (class 1259 OID 191671)
-- Dependencies: 542 3304
-- Name: postitulos_postitulo_nacional_normativa_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_nacional_normativa_postitulo_id ON postitulos_postitulo_nacional USING btree (normativa_postitulo_id);


--
-- TOC entry 2985 (class 1259 OID 191656)
-- Dependencies: 522 3304
-- Name: postitulos_postitulo_tipo_normativa_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulo_tipo_normativa_id ON postitulos_postitulo USING btree (tipo_normativa_id);


--
-- TOC entry 2975 (class 1259 OID 191655)
-- Dependencies: 520 3304
-- Name: postitulos_postitulos_areas_areapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_areas_areapostitulo_id ON postitulos_postitulos_areas USING btree (areapostitulo_id);


--
-- TOC entry 2978 (class 1259 OID 191654)
-- Dependencies: 520 3304
-- Name: postitulos_postitulos_areas_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_areas_postitulo_id ON postitulos_postitulos_areas USING btree (postitulo_id);


--
-- TOC entry 2965 (class 1259 OID 191651)
-- Dependencies: 516 3304
-- Name: postitulos_postitulos_jurisdicciones_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_jurisdicciones_jurisdiccion_id ON postitulos_postitulos_jurisdicciones USING btree (jurisdiccion_id);


--
-- TOC entry 2968 (class 1259 OID 191650)
-- Dependencies: 516 3304
-- Name: postitulos_postitulos_jurisdicciones_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_jurisdicciones_postitulo_id ON postitulos_postitulos_jurisdicciones USING btree (postitulo_id);


--
-- TOC entry 3026 (class 1259 OID 191670)
-- Dependencies: 540 3304
-- Name: postitulos_postitulos_nacionales_carreras_carrerapostitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_nacionales_carreras_carrerapostitulo_id ON postitulos_postitulos_nacionales_carreras USING btree (carrerapostitulo_id);


--
-- TOC entry 3029 (class 1259 OID 191669)
-- Dependencies: 540 3304
-- Name: postitulos_postitulos_nacionales_carreras_postitulonacional_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_nacionales_carreras_postitulonacional_id ON postitulos_postitulos_nacionales_carreras USING btree (postitulonacional_id);


--
-- TOC entry 2969 (class 1259 OID 191653)
-- Dependencies: 518 3304
-- Name: postitulos_postitulos_niveles_nivel_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_niveles_nivel_id ON postitulos_postitulos_niveles USING btree (nivel_id);


--
-- TOC entry 2972 (class 1259 OID 191652)
-- Dependencies: 518 3304
-- Name: postitulos_postitulos_niveles_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_postitulos_niveles_postitulo_id ON postitulos_postitulos_niveles USING btree (postitulo_id);


--
-- TOC entry 3093 (class 1259 OID 191694)
-- Dependencies: 568 3304
-- Name: postitulos_solicitud_anexos_anexo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_anexos_anexo_id ON postitulos_solicitud_anexos USING btree (anexo_id);


--
-- TOC entry 3098 (class 1259 OID 191695)
-- Dependencies: 568 3304
-- Name: postitulos_solicitud_anexos_solicitud_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_anexos_solicitud_id ON postitulos_solicitud_anexos USING btree (solicitud_id);


--
-- TOC entry 3076 (class 1259 OID 191686)
-- Dependencies: 562 3304
-- Name: postitulos_solicitud_carrera_postitulo_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_carrera_postitulo_id ON postitulos_solicitud USING btree (carrera_postitulo_id);


--
-- TOC entry 3089 (class 1259 OID 191692)
-- Dependencies: 566 3304
-- Name: postitulos_solicitud_establecimientos_establecimiento_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_establecimientos_establecimiento_id ON postitulos_solicitud_establecimientos USING btree (establecimiento_id);


--
-- TOC entry 3092 (class 1259 OID 191693)
-- Dependencies: 566 3304
-- Name: postitulos_solicitud_establecimientos_solicitud_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_establecimientos_solicitud_id ON postitulos_solicitud_establecimientos USING btree (solicitud_id);


--
-- TOC entry 3077 (class 1259 OID 191688)
-- Dependencies: 562 3304
-- Name: postitulos_solicitud_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_estado_id ON postitulos_solicitud USING btree (estado_id);


--
-- TOC entry 3137 (class 1259 OID 191707)
-- Dependencies: 584 3304
-- Name: postitulos_solicitud_estados_estado_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_estados_estado_id ON postitulos_solicitud_estados USING btree (estado_id);


--
-- TOC entry 3140 (class 1259 OID 191706)
-- Dependencies: 584 3304
-- Name: postitulos_solicitud_estados_solicitud_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_estados_solicitud_id ON postitulos_solicitud_estados USING btree (solicitud_id);


--
-- TOC entry 3078 (class 1259 OID 191685)
-- Dependencies: 562 3304
-- Name: postitulos_solicitud_jurisdiccion_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_jurisdiccion_id ON postitulos_solicitud USING btree (jurisdiccion_id);


--
-- TOC entry 3072 (class 1259 OID 191684)
-- Dependencies: 560 3304
-- Name: postitulos_solicitud_normativas_jurisdiccionales_normativaposti; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_normativas_jurisdiccionales_normativaposti ON postitulos_solicitud_normativas_jurisdiccionales USING btree (normativapostitulojurisdiccional_id);


--
-- TOC entry 3075 (class 1259 OID 191683)
-- Dependencies: 560 3304
-- Name: postitulos_solicitud_normativas_jurisdiccionales_solicitud_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_normativas_jurisdiccionales_solicitud_id ON postitulos_solicitud_normativas_jurisdiccionales USING btree (solicitud_id);


--
-- TOC entry 3081 (class 1259 OID 191687)
-- Dependencies: 562 3304
-- Name: postitulos_solicitud_postitulo_nacional_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_solicitud_postitulo_nacional_id ON postitulos_solicitud USING btree (postitulo_nacional_id);


--
-- TOC entry 3082 (class 1259 OID 191690)
-- Dependencies: 564 3304
-- Name: postitulos_validez_nacional_cue; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_validez_nacional_cue ON postitulos_validez_nacional USING btree (cue);


--
-- TOC entry 3083 (class 1259 OID 191691)
-- Dependencies: 564 3304
-- Name: postitulos_validez_nacional_cue_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_validez_nacional_cue_like ON postitulos_validez_nacional USING btree (cue varchar_pattern_ops);


--
-- TOC entry 3086 (class 1259 OID 191689)
-- Dependencies: 564 3304
-- Name: postitulos_validez_nacional_solicitud_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX postitulos_validez_nacional_solicitud_id ON postitulos_validez_nacional USING btree (solicitud_id);


--
-- TOC entry 3141 (class 2606 OID 190963)
-- Dependencies: 2945 506 504 3304
-- Name: carrerapostitulo_id_refs_id_5048cd6d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT carrerapostitulo_id_refs_id_5048cd6d FOREIGN KEY (carrerapostitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3156 (class 2606 OID 191180)
-- Dependencies: 3010 532 530 3304
-- Name: carrerapostitulojurisdiccional_id_refs_id_e6bbeee; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT carrerapostitulojurisdiccional_id_refs_id_e6bbeee FOREIGN KEY (carrerapostitulojurisdiccional_id) REFERENCES postitulos_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3146 (class 2606 OID 191087)
-- Dependencies: 2983 522 516 3304
-- Name: postitulo_id_refs_id_338418db; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulo_id_refs_id_338418db FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3148 (class 2606 OID 191092)
-- Dependencies: 2983 522 518 3304
-- Name: postitulo_id_refs_id_39dcf8a4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulo_id_refs_id_39dcf8a4 FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3150 (class 2606 OID 191097)
-- Dependencies: 2983 522 520 3304
-- Name: postitulo_id_refs_id_411f3970; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulo_id_refs_id_411f3970 FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3165 (class 2606 OID 191269)
-- Dependencies: 3034 542 540 3304
-- Name: postitulonacional_id_refs_id_f234084; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulonacional_id_refs_id_f234084 FOREIGN KEY (postitulonacional_id) REFERENCES postitulos_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3162 (class 2606 OID 191193)
-- Dependencies: 3010 532 534 3304
-- Name: postitulos_carrera_postitulo__carrera_postitulo_jurisdicci_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo__carrera_postitulo_jurisdicci_fkey FOREIGN KEY (carrera_postitulo_jurisdiccional_id) REFERENCES postitulos_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3145 (class 2606 OID 190976)
-- Dependencies: 2945 506 508 3304
-- Name: postitulos_carrera_postitulo_estados_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3144 (class 2606 OID 190981)
-- Dependencies: 2936 502 508 3304
-- Name: postitulos_carrera_postitulo_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3160 (class 2606 OID 191165)
-- Dependencies: 2945 506 532 3304
-- Name: postitulos_carrera_postitulo_jurisdic_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdic_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3159 (class 2606 OID 191170)
-- Dependencies: 305 532 3304
-- Name: postitulos_carrera_postitulo_jurisdicciona_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdicciona_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3161 (class 2606 OID 191198)
-- Dependencies: 2988 524 534 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_esta_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_esta_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3158 (class 2606 OID 191175)
-- Dependencies: 2988 524 532 3304
-- Name: postitulos_carrera_postitulo_jurisdiccional_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrera_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_carrera_postitulo_jurisdiccional_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3143 (class 2606 OID 190958)
-- Dependencies: 2936 502 506 3304
-- Name: postitulos_carrerapostitulo_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carrerapostitulo
    ADD CONSTRAINT postitulos_carrerapostitulo_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_carrera_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3142 (class 2606 OID 190942)
-- Dependencies: 305 504 3304
-- Name: postitulos_carreras_postitulo_jurisdiccion_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulo_jurisdicciones
    ADD CONSTRAINT postitulos_carreras_postitulo_jurisdiccion_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3157 (class 2606 OID 191150)
-- Dependencies: 2997 528 530 3304
-- Name: postitulos_carreras_postitulos_norma_normativapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_carreras_postitulos_normativas
    ADD CONSTRAINT postitulos_carreras_postitulos_norma_normativapostitulo_id_fkey FOREIGN KEY (normativapostitulo_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3190 (class 2606 OID 191514)
-- Dependencies: 3010 532 570 3304
-- Name: postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohorte_postitulo
    ADD CONSTRAINT postitulos_cohorte_postitulo_carrera_postitulo_jurisdiccio_fkey FOREIGN KEY (carrera_postitulo_jurisdiccional_id) REFERENCES postitulos_carrera_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3196 (class 2606 OID 191576)
-- Dependencies: 174 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_anexo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos
    ADD CONSTRAINT postitulos_cohortes_postitulo_anexos_anexo_id_fkey FOREIGN KEY (anexo_id) REFERENCES registro_anexo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3195 (class 2606 OID 191581)
-- Dependencies: 3102 570 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_cohorte_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos
    ADD CONSTRAINT postitulos_cohortes_postitulo_anexos_cohorte_postitulo_id_fkey FOREIGN KEY (cohorte_postitulo_id) REFERENCES postitulos_cohorte_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3194 (class 2606 OID 191586)
-- Dependencies: 3117 576 578 3304
-- Name: postitulos_cohortes_postitulo_anexos_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_anexos
    ADD CONSTRAINT postitulos_cohortes_postitulo_anexos_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_cohorte_postitulo_anexo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3192 (class 2606 OID 191545)
-- Dependencies: 3102 570 574 3304
-- Name: postitulos_cohortes_postitulo_estable_cohorte_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos
    ADD CONSTRAINT postitulos_cohortes_postitulo_estable_cohorte_postitulo_id_fkey FOREIGN KEY (cohorte_postitulo_id) REFERENCES postitulos_cohorte_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3193 (class 2606 OID 191540)
-- Dependencies: 221 574 3304
-- Name: postitulos_cohortes_postitulo_estableci_establecimiento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos
    ADD CONSTRAINT postitulos_cohortes_postitulo_estableci_establecimiento_id_fkey FOREIGN KEY (establecimiento_id) REFERENCES registro_establecimiento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3191 (class 2606 OID 191550)
-- Dependencies: 3106 572 574 3304
-- Name: postitulos_cohortes_postitulo_establecimientos_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_establecimientos
    ADD CONSTRAINT postitulos_cohortes_postitulo_establecimientos_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_cohorte_postitulo_establecimiento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3198 (class 2606 OID 191617)
-- Dependencies: 3102 570 582 3304
-- Name: postitulos_cohortes_postitulo_extensi_cohorte_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas
    ADD CONSTRAINT postitulos_cohortes_postitulo_extensi_cohorte_postitulo_id_fkey FOREIGN KEY (cohorte_postitulo_id) REFERENCES postitulos_cohorte_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3199 (class 2606 OID 191612)
-- Dependencies: 266 582 3304
-- Name: postitulos_cohortes_postitulo_extensio_extension_aulica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas
    ADD CONSTRAINT postitulos_cohortes_postitulo_extensio_extension_aulica_id_fkey FOREIGN KEY (extension_aulica_id) REFERENCES registro_extension_aulica(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3197 (class 2606 OID 191622)
-- Dependencies: 3128 580 582 3304
-- Name: postitulos_cohortes_postitulo_extensiones_aulica_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_cohortes_postitulo_extensiones_aulicas
    ADD CONSTRAINT postitulos_cohortes_postitulo_extensiones_aulica_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_cohorte_postitulo_extension_aulica(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3155 (class 2606 OID 191135)
-- Dependencies: 2992 526 528 3304
-- Name: postitulos_normativa_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa
    ADD CONSTRAINT postitulos_normativa_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3178 (class 2606 OID 191376)
-- Dependencies: 3059 554 556 3304
-- Name: postitulos_normativa_postitul_normativa_postitulo_jurisdic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_normativa_postitul_normativa_postitulo_jurisdic_fkey FOREIGN KEY (normativa_postitulo_jurisdiccional_id) REFERENCES postitulos_normativa_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3176 (class 2606 OID 191348)
-- Dependencies: 3046 548 554 3304
-- Name: postitulos_normativa_postitul_tipo_normativa_postitulo_jur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_normativa_postitul_tipo_normativa_postitulo_jur_fkey FOREIGN KEY (tipo_normativa_postitulo_jurisdiccional_id) REFERENCES postitulos_tipo_normativa_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3175 (class 2606 OID 191353)
-- Dependencies: 305 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccio_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccio_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3174 (class 2606 OID 191358)
-- Dependencies: 3050 550 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccio_otorgada_por_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccio_otorgada_por_id_fkey FOREIGN KEY (otorgada_por_id) REFERENCES postitulos_normativa_motivo_otorgamiento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3177 (class 2606 OID 191381)
-- Dependencies: 3054 552 556 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_es_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional_estados
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccional_es_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3173 (class 2606 OID 191363)
-- Dependencies: 3054 552 554 3304
-- Name: postitulos_normativa_postitulo_jurisdiccional_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulo_jurisdiccional
    ADD CONSTRAINT postitulos_normativa_postitulo_jurisdiccional_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3172 (class 2606 OID 191300)
-- Dependencies: 2997 528 546 3304
-- Name: postitulos_normativa_postitulos_est_normativa_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_est_normativa_postitulo_id_fkey FOREIGN KEY (normativa_postitulo_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3171 (class 2606 OID 191305)
-- Dependencies: 2992 526 546 3304
-- Name: postitulos_normativa_postitulos_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_normativa_postitulos_estados
    ADD CONSTRAINT postitulos_normativa_postitulos_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_normativa_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3153 (class 2606 OID 191077)
-- Dependencies: 2945 506 522 3304
-- Name: postitulos_postitulo_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3152 (class 2606 OID 191082)
-- Dependencies: 2953 510 522 3304
-- Name: postitulos_postitulo_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3163 (class 2606 OID 191226)
-- Dependencies: 2953 510 538 3304
-- Name: postitulos_postitulo_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3164 (class 2606 OID 191221)
-- Dependencies: 2983 522 538 3304
-- Name: postitulos_postitulo_estados_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_estados
    ADD CONSTRAINT postitulos_postitulo_estados_postitulo_id_fkey FOREIGN KEY (postitulo_id) REFERENCES postitulos_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3167 (class 2606 OID 191264)
-- Dependencies: 3018 536 542 3304
-- Name: postitulos_postitulo_nacional_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3170 (class 2606 OID 191282)
-- Dependencies: 3034 542 544 3304
-- Name: postitulos_postitulo_nacional_estado_postitulo_nacional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estado_postitulo_nacional_id_fkey FOREIGN KEY (postitulo_nacional_id) REFERENCES postitulos_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3169 (class 2606 OID 191287)
-- Dependencies: 3018 536 544 3304
-- Name: postitulos_postitulo_nacional_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional_estados
    ADD CONSTRAINT postitulos_postitulo_nacional_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3168 (class 2606 OID 191259)
-- Dependencies: 2997 528 542 3304
-- Name: postitulos_postitulo_nacional_normativa_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo_nacional
    ADD CONSTRAINT postitulos_postitulo_nacional_normativa_postitulo_id_fkey FOREIGN KEY (normativa_postitulo_id) REFERENCES postitulos_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3154 (class 2606 OID 191072)
-- Dependencies: 2961 514 522 3304
-- Name: postitulos_postitulo_tipo_normativa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulo
    ADD CONSTRAINT postitulos_postitulo_tipo_normativa_id_fkey FOREIGN KEY (tipo_normativa_id) REFERENCES postitulos_tipo_normativa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3151 (class 2606 OID 191056)
-- Dependencies: 2932 500 520 3304
-- Name: postitulos_postitulos_areas_areapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_areas
    ADD CONSTRAINT postitulos_postitulos_areas_areapostitulo_id_fkey FOREIGN KEY (areapostitulo_id) REFERENCES postitulos_area_postitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3147 (class 2606 OID 191026)
-- Dependencies: 305 516 3304
-- Name: postitulos_postitulos_jurisdicciones_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_jurisdicciones
    ADD CONSTRAINT postitulos_postitulos_jurisdicciones_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3166 (class 2606 OID 191241)
-- Dependencies: 2945 506 540 3304
-- Name: postitulos_postitulos_nacionales_carre_carrerapostitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_nacionales_carreras
    ADD CONSTRAINT postitulos_postitulos_nacionales_carre_carrerapostitulo_id_fkey FOREIGN KEY (carrerapostitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3149 (class 2606 OID 191041)
-- Dependencies: 309 518 3304
-- Name: postitulos_postitulos_niveles_nivel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_postitulos_niveles
    ADD CONSTRAINT postitulos_postitulos_niveles_nivel_id_fkey FOREIGN KEY (nivel_id) REFERENCES registro_nivel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3189 (class 2606 OID 191493)
-- Dependencies: 174 568 3304
-- Name: postitulos_solicitud_anexos_anexo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_anexos
    ADD CONSTRAINT postitulos_solicitud_anexos_anexo_id_fkey FOREIGN KEY (anexo_id) REFERENCES registro_anexo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3188 (class 2606 OID 191498)
-- Dependencies: 3079 562 568 3304
-- Name: postitulos_solicitud_anexos_solicitud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_anexos
    ADD CONSTRAINT postitulos_solicitud_anexos_solicitud_id_fkey FOREIGN KEY (solicitud_id) REFERENCES postitulos_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3182 (class 2606 OID 191426)
-- Dependencies: 2945 506 562 3304
-- Name: postitulos_solicitud_carrera_postitulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud
    ADD CONSTRAINT postitulos_solicitud_carrera_postitulo_id_fkey FOREIGN KEY (carrera_postitulo_id) REFERENCES postitulos_carrerapostitulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3187 (class 2606 OID 191473)
-- Dependencies: 221 566 3304
-- Name: postitulos_solicitud_establecimientos_establecimiento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_establecimientos
    ADD CONSTRAINT postitulos_solicitud_establecimientos_establecimiento_id_fkey FOREIGN KEY (establecimiento_id) REFERENCES registro_establecimiento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3186 (class 2606 OID 191478)
-- Dependencies: 3079 562 566 3304
-- Name: postitulos_solicitud_establecimientos_solicitud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_establecimientos
    ADD CONSTRAINT postitulos_solicitud_establecimientos_solicitud_id_fkey FOREIGN KEY (solicitud_id) REFERENCES postitulos_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3184 (class 2606 OID 191436)
-- Dependencies: 3068 558 562 3304
-- Name: postitulos_solicitud_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud
    ADD CONSTRAINT postitulos_solicitud_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3200 (class 2606 OID 191640)
-- Dependencies: 3068 558 584 3304
-- Name: postitulos_solicitud_estados_estado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_estados
    ADD CONSTRAINT postitulos_solicitud_estados_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES postitulos_estado_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3201 (class 2606 OID 191635)
-- Dependencies: 3079 562 584 3304
-- Name: postitulos_solicitud_estados_solicitud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_estados
    ADD CONSTRAINT postitulos_solicitud_estados_solicitud_id_fkey FOREIGN KEY (solicitud_id) REFERENCES postitulos_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3181 (class 2606 OID 191421)
-- Dependencies: 305 562 3304
-- Name: postitulos_solicitud_jurisdiccion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud
    ADD CONSTRAINT postitulos_solicitud_jurisdiccion_id_fkey FOREIGN KEY (jurisdiccion_id) REFERENCES registro_jurisdiccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3180 (class 2606 OID 191406)
-- Dependencies: 3059 554 560 3304
-- Name: postitulos_solicitud_normativ_normativapostitulojurisdicci_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_normativas_jurisdiccionales
    ADD CONSTRAINT postitulos_solicitud_normativ_normativapostitulojurisdicci_fkey FOREIGN KEY (normativapostitulojurisdiccional_id) REFERENCES postitulos_normativa_postitulo_jurisdiccional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3183 (class 2606 OID 191431)
-- Dependencies: 3034 542 562 3304
-- Name: postitulos_solicitud_postitulo_nacional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud
    ADD CONSTRAINT postitulos_solicitud_postitulo_nacional_id_fkey FOREIGN KEY (postitulo_nacional_id) REFERENCES postitulos_postitulo_nacional(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3185 (class 2606 OID 191458)
-- Dependencies: 3079 562 564 3304
-- Name: postitulos_validez_nacional_solicitud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_validez_nacional
    ADD CONSTRAINT postitulos_validez_nacional_solicitud_id_fkey FOREIGN KEY (solicitud_id) REFERENCES postitulos_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3179 (class 2606 OID 191441)
-- Dependencies: 3079 562 560 3304
-- Name: solicitud_id_refs_id_62904eaa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY postitulos_solicitud_normativas_jurisdiccionales
    ADD CONSTRAINT solicitud_id_refs_id_62904eaa FOREIGN KEY (solicitud_id) REFERENCES postitulos_solicitud(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2014-06-02 15:00:50 ART

--
-- PostgreSQL database dump complete
--


-----------------------
INSERT INTO postitulos_estado_carrera_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_carrera_postitulo_jurisdiccional (nombre) VALUES ('Sin controlar'), ('Controlado'), ('Registrado');
INSERT INTO postitulos_estado_postitulo_nacional (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_normativa_postitulo (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_estado_normativa_postitulo_jurisdiccional (nombre) VALUES ('Vigente'), ('No vigente');
INSERT INTO postitulos_normativa_motivo_otorgamiento (nombre) VALUES ('Aprobación'), ('Implementación'), ('Aprobación/Implementación');
INSERT INTO postitulos_tipo_normativa_postitulo_jurisdiccional (nombre) VALUES ('Resolución'), ('Decreto'), ('Disposición'), ('Actuación'), ('Acuerdo'), ('Circular');
INSERT INTO postitulos_estado_solicitud (nombre) VALUES ('Controlado'), ('Numerado'), ('Pendiente');


-----------------------

INSERT INTO deltas_sql (numero, app, comentario) VALUES ('132', 'Postítulos', 'Aplicación de postítulos - #406');

COMMIT;
