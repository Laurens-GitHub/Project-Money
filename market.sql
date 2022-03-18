--
-- PostgreSQL database dump
--

-- Dumped from database version 13.6 (Ubuntu 13.6-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.6 (Ubuntu 13.6-1.pgdg20.04+1)

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
    stock_id integer NOT NULL,
    user_id integer NOT NULL,
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
38	UBML	 Ubermelon Co
\.


--
-- Data for Name: user_stocks; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.user_stocks (user_stock_id, stock_id, user_id, date_saved) FROM stdin;
1	4	1	03/18/22
2	11	1	03/18/22
3	17	1	03/18/22
4	27	1	03/18/22
5	30	1	03/18/22
6	25	1	03/18/22
7	23	1	03/18/22
8	14	1	03/18/22
9	35	1	03/18/22
10	8	1	03/18/22
11	26	2	03/18/22
12	29	2	03/18/22
13	13	2	03/18/22
14	37	2	03/18/22
15	30	2	03/18/22
16	2	2	03/18/22
17	7	2	03/18/22
18	12	2	03/18/22
19	15	2	03/18/22
20	36	2	03/18/22
21	8	3	03/18/22
22	30	3	03/18/22
23	2	3	03/18/22
24	4	3	03/18/22
25	24	3	03/18/22
26	34	3	03/18/22
27	19	3	03/18/22
28	35	3	03/18/22
29	5	3	03/18/22
30	16	3	03/18/22
31	3	4	03/18/22
32	22	4	03/18/22
33	37	4	03/18/22
34	2	4	03/18/22
35	23	4	03/18/22
36	6	4	03/18/22
37	21	4	03/18/22
38	7	4	03/18/22
39	35	4	03/18/22
40	27	4	03/18/22
41	27	5	03/18/22
42	6	5	03/18/22
43	18	5	03/18/22
44	5	5	03/18/22
45	36	5	03/18/22
46	8	5	03/18/22
47	21	5	03/18/22
48	33	5	03/18/22
49	30	5	03/18/22
50	37	5	03/18/22
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

SELECT pg_catalog.setval('public.stocks_stock_id_seq', 38, true);


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
-- Name: user_stocks unique_user_stock; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_stocks
    ADD CONSTRAINT unique_user_stock UNIQUE (user_id, stock_id);


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

