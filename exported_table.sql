--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Ubuntu 16.3-1.pgdg22.04+1)
-- Dumped by pg_dump version 16.3 (Ubuntu 16.3-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: anime_videos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anime_videos (
    user_id bigint,
    url text,
    service text
);


--
-- Name: misc_videos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.misc_videos (
    user_id bigint,
    url text,
    service text
);


--
-- Name: music; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.music (
    user_id bigint,
    url text,
    service text
);


--
-- Name: tech_videos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tech_videos (
    user_id bigint,
    url text,
    service text
);


--
-- Name: to_watch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.to_watch (
    user_id bigint,
    url text,
    service text
);


--
-- Name: watched_videos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.watched_videos (
    user_id bigint,
    url text,
    service text
);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

