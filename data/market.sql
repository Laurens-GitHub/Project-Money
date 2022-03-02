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
    date_saved character varying
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
1	7	1	02/25/22
2	32	1	02/25/22
3	2	1	02/25/22
4	8	1	02/25/22
5	6	1	02/25/22
6	9	1	02/25/22
7	20	1	02/25/22
8	13	1	02/25/22
9	2	1	02/25/22
10	36	1	02/25/22
11	3	2	02/25/22
12	37	2	02/25/22
13	8	2	02/25/22
14	2	2	02/25/22
15	37	2	02/25/22
16	14	2	02/25/22
17	37	2	02/25/22
18	34	2	02/25/22
19	1	2	02/25/22
20	3	2	02/25/22
21	32	3	02/25/22
22	26	3	02/25/22
23	33	3	02/25/22
24	2	3	02/25/22
25	21	3	02/25/22
26	2	3	02/25/22
27	15	3	02/25/22
28	15	3	02/25/22
29	17	3	02/25/22
30	12	3	02/25/22
31	23	4	02/25/22
32	27	4	02/25/22
33	6	4	02/25/22
34	7	4	02/25/22
35	1	4	02/25/22
36	30	4	02/25/22
37	12	4	02/25/22
38	2	4	02/25/22
39	22	4	02/25/22
40	31	4	02/25/22
41	26	5	02/25/22
42	19	5	02/25/22
43	20	5	02/25/22
44	20	5	02/25/22
45	28	5	02/25/22
46	18	5	02/25/22
47	4	5	02/25/22
48	26	5	02/25/22
49	25	5	02/25/22
50	17	5	02/25/22
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

