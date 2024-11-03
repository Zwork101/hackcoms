--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: idea_contributor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.idea_contributor (
    idea_id integer,
    user_id integer,
    id integer NOT NULL
);


ALTER TABLE public.idea_contributor OWNER TO postgres;

--
-- Name: idea_contributor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.idea_contributor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.idea_contributor_id_seq OWNER TO postgres;

--
-- Name: idea_contributor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.idea_contributor_id_seq OWNED BY public.idea_contributor.id;


--
-- Name: idea_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.idea_roles (
    idea_id integer,
    role_id integer,
    id integer NOT NULL
);


ALTER TABLE public.idea_roles OWNER TO postgres;

--
-- Name: idea_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.idea_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.idea_roles_id_seq OWNER TO postgres;

--
-- Name: idea_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.idea_roles_id_seq OWNED BY public.idea_roles.id;


--
-- Name: ideas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ideas (
    owner_id integer,
    name character varying NOT NULL,
    description character varying NOT NULL,
    asl_fluent_only boolean NOT NULL,
    started boolean NOT NULL,
    searching_for_contributors boolean NOT NULL,
    finished boolean NOT NULL,
    creation_date timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.ideas OWNER TO postgres;

--
-- Name: ideas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ideas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ideas_id_seq OWNER TO postgres;

--
-- Name: ideas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ideas_id_seq OWNED BY public.ideas.id;


--
-- Name: invite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invite (
    idea_id integer,
    target_id integer,
    id integer NOT NULL
);


ALTER TABLE public.invite OWNER TO postgres;

--
-- Name: invite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invite_id_seq OWNER TO postgres;

--
-- Name: invite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invite_id_seq OWNED BY public.invite.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    room_id integer,
    sender_id integer,
    invite_id integer,
    content character varying NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_id_seq OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    role_name character varying NOT NULL,
    role_description character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_id_seq OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room (
    id integer NOT NULL
);


ALTER TABLE public.room OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.room_id_seq OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;


--
-- Name: user_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_account (
    username character varying NOT NULL,
    password bytea NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    hearing_impaired boolean NOT NULL,
    need_interpreter boolean NOT NULL,
    understand_asl boolean NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.user_account OWNER TO postgres;

--
-- Name: user_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_account_id_seq OWNER TO postgres;

--
-- Name: user_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_account_id_seq OWNED BY public.user_account.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_id integer,
    role_id integer,
    id integer NOT NULL
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_roles_id_seq OWNER TO postgres;

--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: user_room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_room (
    user_id integer,
    room_id integer,
    id integer NOT NULL
);


ALTER TABLE public.user_room OWNER TO postgres;

--
-- Name: user_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_room_id_seq OWNER TO postgres;

--
-- Name: user_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_room_id_seq OWNED BY public.user_room.id;


--
-- Name: idea_contributor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_contributor ALTER COLUMN id SET DEFAULT nextval('public.idea_contributor_id_seq'::regclass);


--
-- Name: idea_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_roles ALTER COLUMN id SET DEFAULT nextval('public.idea_roles_id_seq'::regclass);


--
-- Name: ideas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ideas ALTER COLUMN id SET DEFAULT nextval('public.ideas_id_seq'::regclass);


--
-- Name: invite id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invite ALTER COLUMN id SET DEFAULT nextval('public.invite_id_seq'::regclass);


--
-- Name: message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);


--
-- Name: user_account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_account ALTER COLUMN id SET DEFAULT nextval('public.user_account_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: user_room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_room ALTER COLUMN id SET DEFAULT nextval('public.user_room_id_seq'::regclass);


--
-- Data for Name: idea_contributor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.idea_contributor (idea_id, user_id, id) FROM stdin;
5	2	1
1	2	2
5	5	3
1	5	4
2	5	5
3	5	6
4	5	7
4	7	8
1	2	9
\.


--
-- Data for Name: idea_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.idea_roles (idea_id, role_id, id) FROM stdin;
1	1	1
1	2	2
1	9	3
1	10	4
2	2	5
2	7	6
3	2	7
3	4	8
3	5	9
4	3	10
4	6	11
4	7	12
4	8	13
4	9	14
5	1	15
5	2	16
5	3	17
5	4	18
5	8	19
5	10	20
\.


--
-- Data for Name: ideas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ideas (owner_id, name, description, asl_fluent_only, started, searching_for_contributors, finished, creation_date, id) FROM stdin;
4	New Encryption Algorith	With the rise of super computers and quantum compusters, we need an encryption algorithm that will last! Plus, we need to push businesses to use the algorithm we invent!	f	f	t	f	2024-11-03 14:27:16.511786+00	3
6	Fun JRPG about Villans	I think being a villan is pretty neat, but most games are all about heros! I want to make a MMO RPG about Villans doing evviiiilllll :)	f	f	t	f	2024-11-03 14:28:38.898827+00	4
7	Website to track attendance	We want a website to track how many times our members have gone to our events to reward them with swag!	f	f	t	f	2024-11-03 14:30:24.971656+00	5
1	Calender App	I've always wanted to build a Calender app based on the Mayan calender. We would need to restart it since it ended, but I have some ideas on how to get around that.	f	f	f	t	2024-11-03 14:07:57.803582+00	1
2	Discord Library	I've been wanting to make a discord bot, but I don't like any of the existing python libraries for it. Anyone want to make our own?	f	f	f	t	2024-11-03 14:11:10.561434+00	2
\.


--
-- Data for Name: invite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invite (idea_id, target_id, id) FROM stdin;
5	2	1
5	5	2
1	2	3
2	5	4
2	1	5
3	5	6
4	7	7
4	5	8
1	5	9
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.message (room_id, sender_id, invite_id, content, "timestamp", id) FROM stdin;
2	7	1	Project Invite for Website to track attendance 👍	2024-11-03 14:31:38.268416+00	1
3	5	\N	Hey, can I help?	2024-11-03 14:32:20.684317+00	2
3	7	2	Project Invite for Website to track attendance 👍	2024-11-03 14:32:44.96458+00	3
4	7	\N	I'll help you!	2024-11-03 14:33:11.694864+00	4
5	5	\N	I'd move to help!	2024-11-03 14:34:11.681821+00	5
6	5	\N	I'd love to help!	2024-11-03 14:34:21.50743+00	6
7	5	\N	I'd move to help!	2024-11-03 14:34:33.420654+00	7
8	1	3	Project Invite for Calender App 👍	2024-11-03 14:35:10.204134+00	8
6	2	4	Project Invite for Discord Library 👍	2024-11-03 14:36:08.085166+00	9
8	2	5	Project Invite for Discord Library 👍	2024-11-03 14:36:18.486812+00	10
7	4	6	Project Invite for New Encryption Algorith 👍	2024-11-03 14:37:12.66596+00	11
4	6	7	Project Invite for Fun JRPG about Villans 👍	2024-11-03 14:37:57.49605+00	12
9	5	\N	I'll help you!	2024-11-03 14:38:18.878036+00	13
9	6	8	Project Invite for Fun JRPG about Villans 👍	2024-11-03 14:39:40.485625+00	14
5	1	9	Project Invite for Calender App 👍	2024-11-03 14:40:12.413636+00	15
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (role_name, role_description, id) FROM stdin;
Frontend Dev	lowenfowno	1
Backkend Dev	lowenfowno	2
Designer	lowenfowno	3
Business	lowenfowno	4
Cybersecurity	lowenfowno	5
Graphic Designer	lowenfowno	6
Game Dev	lowenfowno	7
Mobile Dev	lowenfowno	8
Network Engineer	lowenfowno	9
Sys Admin	lowenfowno	10
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room (id) FROM stdin;
1
2
3
4
5
6
7
8
9
10
\.


--
-- Data for Name: user_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_account (username, password, first_name, last_name, hearing_impaired, need_interpreter, understand_asl, id) FROM stdin;
evan	\\x7363727970743a33323736383a383a312450624444716c55336d334645464f7073243861323765666362313234633732643166386361666139363863386165386161373265623064626466333433653564363961633638613163396331613138326531636638366436313138613465336639346466633136636566376638363539343761633539386134376530313865386239396639306464386236386638393866		zwack	f	f	f	1
nathan	\\x7363727970743a33323736383a383a31244b435356577255664542424467485a6c243037663835303262303437643433343362633065636565386166326532373836643365313564633430656264646439613935643734643135646137333332333863306632653336626431643032623038373339313464653566623634353166646632383739353337346237353166303963393038616237356366313837633539	Nathan	Zilora	f	f	f	2
bob	\\x7363727970743a33323736383a383a31245453484f3237344e6d63366366695946246264636264313736376531346266386239316361656236363234623430613166303535396530613764383461323730313361663636303935303331356561346565353761653735646162356434343563376235333838383839323465623434373563306635353430616162383236346237323636663561613735343332633531	Bob	Smith	t	f	f	3
alice	\\x7363727970743a33323736383a383a31244d59786638697036304e486744366f43243566323738303366636563343036653939613936313065303739643132333833633066346131323137343934633763356561346437666666316236623563376330333764626132636465363063343162386337326239303365333539313566313166386461653832386137323138386435363061336230383230326561623635	Alice	Smith	f	f	f	4
hero	\\x7363727970743a33323736383a383a312455377a3278354169506f41457552564f243636373032303834633439326135343931653934613734636564383136356564656565316232326137616638323665663037333838363532306635346139356631653765643630333535653732323261346331336665313237366366353334373232366436633531366431313561623664353565356562663266313661353761	zwack	zwack	t	t	f	5
villan	\\x7363727970743a33323736383a383a31246b6e397663305279534248424f794145246230306239623163363435336264323236363964373333313232643462663861376461346231376535646236613831366366333930306538366538313361646561623331663361383334626634336533316636386633653463346332346135323465626331663930356161356337313533653537613631396565333730613363	zwack	zwack	t	f	f	6
coms	\\x7363727970743a33323736383a383a312445614e6558687a4b6535334d78417944243432663939633266663531393631653330383964313334366661653563396339373230623064633530616661366333303834653534633333333435396363373431343566393562353131376631616334633565303939323561626639663564363437396162393035656565313765626435303233343630623164663835336632	COMS	@ RIT	t	t	f	7
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_id, role_id, id) FROM stdin;
\.


--
-- Data for Name: user_room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_room (user_id, room_id, id) FROM stdin;
1	1	1
3	1	2
2	2	3
7	2	4
7	3	5
5	3	6
6	4	7
7	4	8
1	5	9
5	5	10
2	6	11
5	6	12
4	7	13
5	7	14
2	8	15
1	8	16
6	9	17
5	9	18
4	10	19
3	10	20
\.


--
-- Name: idea_contributor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.idea_contributor_id_seq', 9, true);


--
-- Name: idea_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.idea_roles_id_seq', 20, true);


--
-- Name: ideas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ideas_id_seq', 5, true);


--
-- Name: invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invite_id_seq', 9, true);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_seq', 15, true);


--
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_id_seq', 10, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.room_id_seq', 10, true);


--
-- Name: user_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_account_id_seq', 7, true);


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 1, false);


--
-- Name: user_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_room_id_seq', 20, true);


--
-- Name: idea_contributor idea_contributor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_contributor
    ADD CONSTRAINT idea_contributor_pkey PRIMARY KEY (id);


--
-- Name: idea_roles idea_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_roles
    ADD CONSTRAINT idea_roles_pkey PRIMARY KEY (id);


--
-- Name: ideas ideas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ideas
    ADD CONSTRAINT ideas_pkey PRIMARY KEY (id);


--
-- Name: invite invite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invite
    ADD CONSTRAINT invite_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- Name: user_account user_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_account
    ADD CONSTRAINT user_account_pkey PRIMARY KEY (id);


--
-- Name: user_account user_account_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_account
    ADD CONSTRAINT user_account_username_key UNIQUE (username);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: user_room user_room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_room
    ADD CONSTRAINT user_room_pkey PRIMARY KEY (id);


--
-- Name: idea_contributor idea_contributor_idea_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_contributor
    ADD CONSTRAINT idea_contributor_idea_id_fkey FOREIGN KEY (idea_id) REFERENCES public.ideas(id);


--
-- Name: idea_contributor idea_contributor_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_contributor
    ADD CONSTRAINT idea_contributor_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_account(id);


--
-- Name: idea_roles idea_roles_idea_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_roles
    ADD CONSTRAINT idea_roles_idea_id_fkey FOREIGN KEY (idea_id) REFERENCES public.ideas(id);


--
-- Name: idea_roles idea_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idea_roles
    ADD CONSTRAINT idea_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: ideas ideas_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ideas
    ADD CONSTRAINT ideas_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.user_account(id);


--
-- Name: invite invite_idea_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invite
    ADD CONSTRAINT invite_idea_id_fkey FOREIGN KEY (idea_id) REFERENCES public.ideas(id);


--
-- Name: invite invite_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invite
    ADD CONSTRAINT invite_target_id_fkey FOREIGN KEY (target_id) REFERENCES public.user_account(id);


--
-- Name: message message_invite_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_invite_id_fkey FOREIGN KEY (invite_id) REFERENCES public.invite(id);


--
-- Name: message message_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- Name: message message_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.user_account(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_account(id);


--
-- Name: user_room user_room_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_room
    ADD CONSTRAINT user_room_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- Name: user_room user_room_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_room
    ADD CONSTRAINT user_room_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_account(id);


--
-- PostgreSQL database dump complete
--

