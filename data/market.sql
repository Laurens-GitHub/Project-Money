--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Ubuntu 13.4-4.pgdg20.04+1)
-- Dumped by pg_dump version 13.4 (Ubuntu 13.4-4.pgdg20.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: stocks; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.stocks (
    stock_id integer NOT NULL,
    symbol character varying,
    company character varying
);


ALTER TABLE public.stocks OWNER TO hackbright;

--
-- Name: stocks_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.stocks_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stocks_stock_id_seq OWNER TO hackbright;

--
-- Name: stocks_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.stocks_stock_id_seq OWNED BY public.stocks.stock_id;


--
-- Name: user_stocks; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.user_stocks (
    user_stock_id integer NOT NULL,
    stock_id integer,
    user_id integer,
    date_saved timestamp without time zone
);


ALTER TABLE public.user_stocks OWNER TO hackbright;

--
-- Name: user_stocks_user_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.user_stocks_user_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_stocks_user_stock_id_seq OWNER TO hackbright;

--
-- Name: user_stocks_user_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.user_stocks_user_stock_id_seq OWNED BY public.user_stocks.user_stock_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying,
    last_name character varying,
    email character varying,
    password character varying
);


ALTER TABLE public.users OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: stocks stock_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.stocks ALTER COLUMN stock_id SET DEFAULT nextval('public.stocks_stock_id_seq'::regclass);


--
-- Name: user_stocks user_stock_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_stocks ALTER COLUMN user_stock_id SET DEFAULT nextval('public.user_stocks_user_stock_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: stocks; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.stocks (stock_id, symbol, company) FROM stdin;
1	TSLA	Tesla Inc
2	LIT	Global X Lithium And Battery Tech ETF
3	TXN	Texas Instruments Inc
4	ADI	Analog Devices Inc
5	NVDA	Nvidia Corporation
6	LAC	Lithium Americas Corp
7	TTNDY	Techtronic Industries Company
8	AMD	Advanced Micro Devices Inc
9	AMZN	Amazon.com Inc
10	FB	Meta Platforms Inc
11	ALB	Albemarle Corp
12	SONY	Sony Group Corporation
13	GOOGL	Alphabet Inc
14	ASML	ASML Holding
15	HD	Home Depot Inc
16	WM	Waste Management Inc
17	DHI	Dr Horton Inc
18	PHM	Pulte Group Inc
19	JNJ	Johnson & Johnson
20	GIS	General Mills Inc
21	AVGO	Broadcom Inc
22	NXPI	NXP Semiconductors
23	PG	Procter And Gamble Co
24	BRKB	Berkshire Hathaway Inc Class B
25	MSFT	Microsoft Corp
26	CWEN	Clearway Energy Inc
27	TGAN	Transphorm Inc
28	PEP	Pepsico Inc
29	MRVL	Marvell Technology Inc
30	NTDOY	Nintendo
31	KLAC	KLA Corp
32	TSM	Taiwan Semiconductor Manufacturing
33	INTC	Intel Corp
34	LRCX	Lam Research Corp
35	AAPL	Apple Inc
36	F	Ford Motor Co
37	QCOM	Qualcomm Inc
\.


--
-- Data for Name: user_stocks; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.user_stocks (user_stock_id, stock_id, user_id, date_saved) FROM stdin;
1	14	1	2022-02-12 00:00:00
2	11	1	2022-02-12 00:00:00
3	15	1	2022-02-12 00:00:00
4	25	1	2022-02-12 00:00:00
5	20	1	2022-02-12 00:00:00
6	34	1	2022-02-12 00:00:00
7	29	1	2022-02-12 00:00:00
8	18	1	2022-02-12 00:00:00
9	26	1	2022-02-12 00:00:00
10	17	1	2022-02-12 00:00:00
11	21	2	2022-02-12 00:00:00
12	12	2	2022-02-12 00:00:00
13	10	2	2022-02-12 00:00:00
14	30	2	2022-02-12 00:00:00
15	21	2	2022-02-12 00:00:00
16	13	2	2022-02-12 00:00:00
17	36	2	2022-02-12 00:00:00
18	5	2	2022-02-12 00:00:00
19	29	2	2022-02-12 00:00:00
20	16	2	2022-02-12 00:00:00
21	23	3	2022-02-12 00:00:00
22	12	3	2022-02-12 00:00:00
23	28	3	2022-02-12 00:00:00
24	37	3	2022-02-12 00:00:00
25	17	3	2022-02-12 00:00:00
26	22	3	2022-02-12 00:00:00
27	26	3	2022-02-12 00:00:00
28	33	3	2022-02-12 00:00:00
29	14	3	2022-02-12 00:00:00
30	5	3	2022-02-12 00:00:00
31	1	4	2022-02-12 00:00:00
32	30	4	2022-02-12 00:00:00
33	33	4	2022-02-12 00:00:00
34	1	4	2022-02-12 00:00:00
35	13	4	2022-02-12 00:00:00
36	12	4	2022-02-12 00:00:00
37	21	4	2022-02-12 00:00:00
38	6	4	2022-02-12 00:00:00
39	10	4	2022-02-12 00:00:00
40	17	4	2022-02-12 00:00:00
41	28	5	2022-02-12 00:00:00
42	29	5	2022-02-12 00:00:00
43	33	5	2022-02-12 00:00:00
44	37	5	2022-02-12 00:00:00
45	27	5	2022-02-12 00:00:00
46	2	5	2022-02-12 00:00:00
47	3	5	2022-02-12 00:00:00
48	33	5	2022-02-12 00:00:00
49	8	5	2022-02-12 00:00:00
50	31	5	2022-02-12 00:00:00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.users (user_id, first_name, last_name, email, password) FROM stdin;
1	John	Doe 0	user0@test.com	test
2	John	Doe 1	user1@test.com	test
3	John	Doe 2	user2@test.com	test
4	John	Doe 3	user3@test.com	test
5	John	Doe 4	user4@test.com	test
\.


--
-- Name: stocks_stock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.stocks_stock_id_seq', 37, true);


--
-- Name: user_stocks_user_stock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.user_stocks_user_stock_id_seq', 50, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.users_user_id_seq', 5, true);


--
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (stock_id);


--
-- Name: stocks stocks_symbol_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_symbol_key UNIQUE (symbol);


--
-- Name: user_stocks user_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_stocks
    ADD CONSTRAINT user_stocks_pkey PRIMARY KEY (user_stock_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: user_stocks user_stocks_stock_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_stocks
    ADD CONSTRAINT user_stocks_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(stock_id);


--
-- Name: user_stocks user_stocks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_stocks
    ADD CONSTRAINT user_stocks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

