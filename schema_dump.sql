--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

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
-- Name: accounts; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.accounts (
    id character varying NOT NULL,
    enrollment_id character varying NOT NULL,
    institution_name character varying NOT NULL,
    institution_id character varying NOT NULL,
    type character varying NOT NULL,
    name character varying NOT NULL,
    subtype character varying NOT NULL,
    currency character varying NOT NULL,
    last_four character varying NOT NULL,
    last_updated date NOT NULL,
    status character varying NOT NULL
);


ALTER TABLE public.accounts OWNER TO cardmathdb;

--
-- Name: banks_preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.banks_preferences (
    user_id integer NOT NULL,
    have_banks json,
    preferred_banks json,
    avoid_banks json
);


ALTER TABLE public.banks_preferences OWNER TO cardmathdb;

--
-- Name: business_preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.business_preferences (
    user_id integer NOT NULL,
    business_type json,
    business_size character varying
);


ALTER TABLE public.business_preferences OWNER TO cardmathdb;

--
-- Name: cardratings_scrape; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.cardratings_scrape (
    scrape_id integer NOT NULL,
    credit_cards_id integer,
    name character varying,
    description_used integer,
    unparsed_issuer character varying,
    unparsed_credit_needed character varying,
    unparsed_card_attributes character varying
);


ALTER TABLE public.cardratings_scrape OWNER TO cardmathdb;

--
-- Name: cardratings_scrape_scrape_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.cardratings_scrape_scrape_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cardratings_scrape_scrape_id_seq OWNER TO cardmathdb;

--
-- Name: cardratings_scrape_scrape_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.cardratings_scrape_scrape_id_seq OWNED BY public.cardratings_scrape.scrape_id;


--
-- Name: consumer_preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.consumer_preferences (
    user_id integer NOT NULL,
    favorite_grocery_stores json,
    favorite_general_goods_stores json
);


ALTER TABLE public.consumer_preferences OWNER TO cardmathdb;

--
-- Name: counterparty; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.counterparty (
    id integer NOT NULL,
    name character varying,
    type character varying
);


ALTER TABLE public.counterparty OWNER TO cardmathdb;

--
-- Name: counterparty_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.counterparty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.counterparty_id_seq OWNER TO cardmathdb;

--
-- Name: counterparty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.counterparty_id_seq OWNED BY public.counterparty.id;


--
-- Name: credit_cards; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.credit_cards (
    id integer NOT NULL,
    name character varying NOT NULL,
    issuer character varying,
    reward_category_map json,
    benefits json,
    credit_needed json,
    sign_on_bonus json,
    apr json,
    annual_fee json,
    statement_credit json,
    primary_reward_unit character varying,
    keywords json
);


ALTER TABLE public.credit_cards OWNER TO cardmathdb;

--
-- Name: credit_cards_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.credit_cards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.credit_cards_id_seq OWNER TO cardmathdb;

--
-- Name: credit_cards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.credit_cards_id_seq OWNED BY public.credit_cards.id;


--
-- Name: credit_profile_preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.credit_profile_preferences (
    user_id integer NOT NULL,
    credit_score integer,
    salary integer,
    lifestyle character varying
);


ALTER TABLE public.credit_profile_preferences OWNER TO cardmathdb;

--
-- Name: enrollments; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.enrollments (
    id character varying NOT NULL,
    user_id integer,
    access_token character varying NOT NULL,
    institution_name character varying NOT NULL,
    signatures json NOT NULL,
    last_updated date NOT NULL
);


ALTER TABLE public.enrollments OWNER TO cardmathdb;

--
-- Name: preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.preferences (
    user_id integer NOT NULL
);


ALTER TABLE public.preferences OWNER TO cardmathdb;

--
-- Name: rewards_programs_preferences; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.rewards_programs_preferences (
    user_id integer NOT NULL,
    preferred_rewards_programs json,
    avoid_rewards_programs json
);


ALTER TABLE public.rewards_programs_preferences OWNER TO cardmathdb;

--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.subscriptions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying NOT NULL,
    start_date date,
    end_date date
);


ALTER TABLE public.subscriptions OWNER TO cardmathdb;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscriptions_id_seq OWNER TO cardmathdb;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.subscriptions_id_seq OWNED BY public.subscriptions.id;


--
-- Name: transaction_details; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.transaction_details (
    txn_id character varying NOT NULL,
    counterparty_id integer,
    processing_status character varying NOT NULL,
    category character varying
);


ALTER TABLE public.transaction_details OWNER TO cardmathdb;

--
-- Name: transactions; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.transactions (
    txn_id character varying NOT NULL,
    account_id character varying NOT NULL,
    amount double precision NOT NULL,
    date date NOT NULL,
    description character varying NOT NULL,
    status character varying NOT NULL,
    running_balance double precision,
    type character varying NOT NULL
);


ALTER TABLE public.transactions OWNER TO cardmathdb;

--
-- Name: user_credit_card_association; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.user_credit_card_association (
    user_id integer NOT NULL,
    credit_card_id integer NOT NULL
);


ALTER TABLE public.user_credit_card_association OWNER TO cardmathdb;

--
-- Name: users; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    full_name character varying,
    disabled boolean,
    hashed_password character varying NOT NULL
);


ALTER TABLE public.users OWNER TO cardmathdb;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO cardmathdb;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: wallet_new_card_association; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.wallet_new_card_association (
    wallet_id integer NOT NULL,
    credit_card_id integer NOT NULL,
    is_held boolean NOT NULL
);


ALTER TABLE public.wallet_new_card_association OWNER TO cardmathdb;

--
-- Name: wallets; Type: TABLE; Schema: public; Owner: cardmathdb
--

CREATE TABLE public.wallets (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying NOT NULL,
    last_edited date NOT NULL,
    is_custom boolean
);


ALTER TABLE public.wallets OWNER TO cardmathdb;

--
-- Name: wallets_id_seq; Type: SEQUENCE; Schema: public; Owner: cardmathdb
--

CREATE SEQUENCE public.wallets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.wallets_id_seq OWNER TO cardmathdb;

--
-- Name: wallets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cardmathdb
--

ALTER SEQUENCE public.wallets_id_seq OWNED BY public.wallets.id;


--
-- Name: cardratings_scrape scrape_id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.cardratings_scrape ALTER COLUMN scrape_id SET DEFAULT nextval('public.cardratings_scrape_scrape_id_seq'::regclass);


--
-- Name: counterparty id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.counterparty ALTER COLUMN id SET DEFAULT nextval('public.counterparty_id_seq'::regclass);


--
-- Name: credit_cards id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.credit_cards ALTER COLUMN id SET DEFAULT nextval('public.credit_cards_id_seq'::regclass);


--
-- Name: subscriptions id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.subscriptions ALTER COLUMN id SET DEFAULT nextval('public.subscriptions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: wallets id; Type: DEFAULT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallets ALTER COLUMN id SET DEFAULT nextval('public.wallets_id_seq'::regclass);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: banks_preferences banks_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.banks_preferences
    ADD CONSTRAINT banks_preferences_pkey PRIMARY KEY (user_id);


--
-- Name: business_preferences business_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.business_preferences
    ADD CONSTRAINT business_preferences_pkey PRIMARY KEY (user_id);


--
-- Name: cardratings_scrape cardratings_scrape_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.cardratings_scrape
    ADD CONSTRAINT cardratings_scrape_pkey PRIMARY KEY (scrape_id);


--
-- Name: consumer_preferences consumer_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.consumer_preferences
    ADD CONSTRAINT consumer_preferences_pkey PRIMARY KEY (user_id);


--
-- Name: counterparty counterparty_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.counterparty
    ADD CONSTRAINT counterparty_pkey PRIMARY KEY (id);


--
-- Name: credit_cards credit_cards_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.credit_cards
    ADD CONSTRAINT credit_cards_pkey PRIMARY KEY (id);


--
-- Name: credit_profile_preferences credit_profile_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.credit_profile_preferences
    ADD CONSTRAINT credit_profile_preferences_pkey PRIMARY KEY (user_id);


--
-- Name: enrollments enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (id);


--
-- Name: preferences preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.preferences
    ADD CONSTRAINT preferences_pkey PRIMARY KEY (user_id);


--
-- Name: rewards_programs_preferences rewards_programs_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.rewards_programs_preferences
    ADD CONSTRAINT rewards_programs_preferences_pkey PRIMARY KEY (user_id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: transaction_details transaction_details_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.transaction_details
    ADD CONSTRAINT transaction_details_pkey PRIMARY KEY (txn_id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (txn_id);


--
-- Name: user_credit_card_association user_credit_card_association_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.user_credit_card_association
    ADD CONSTRAINT user_credit_card_association_pkey PRIMARY KEY (user_id, credit_card_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: wallet_new_card_association wallet_new_card_association_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallet_new_card_association
    ADD CONSTRAINT wallet_new_card_association_pkey PRIMARY KEY (wallet_id, credit_card_id);


--
-- Name: wallets wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_pkey PRIMARY KEY (id);


--
-- Name: ix_accounts_id; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_accounts_id ON public.accounts USING btree (id);


--
-- Name: ix_subscriptions_id; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_subscriptions_id ON public.subscriptions USING btree (id);


--
-- Name: ix_transactions_account_id; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_transactions_account_id ON public.transactions USING btree (account_id);


--
-- Name: ix_transactions_date; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_transactions_date ON public.transactions USING btree (date);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: ix_wallets_id; Type: INDEX; Schema: public; Owner: cardmathdb
--

CREATE INDEX ix_wallets_id ON public.wallets USING btree (id);


--
-- Name: accounts accounts_enrollment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_enrollment_id_fkey FOREIGN KEY (enrollment_id) REFERENCES public.enrollments(id);


--
-- Name: banks_preferences banks_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.banks_preferences
    ADD CONSTRAINT banks_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.preferences(user_id);


--
-- Name: business_preferences business_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.business_preferences
    ADD CONSTRAINT business_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.preferences(user_id);


--
-- Name: cardratings_scrape cardratings_scrape_credit_cards_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.cardratings_scrape
    ADD CONSTRAINT cardratings_scrape_credit_cards_id_fkey FOREIGN KEY (credit_cards_id) REFERENCES public.credit_cards(id);


--
-- Name: consumer_preferences consumer_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.consumer_preferences
    ADD CONSTRAINT consumer_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.preferences(user_id);


--
-- Name: credit_profile_preferences credit_profile_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.credit_profile_preferences
    ADD CONSTRAINT credit_profile_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.preferences(user_id);


--
-- Name: enrollments enrollments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: preferences preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.preferences
    ADD CONSTRAINT preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: rewards_programs_preferences rewards_programs_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.rewards_programs_preferences
    ADD CONSTRAINT rewards_programs_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.preferences(user_id);


--
-- Name: subscriptions subscriptions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: transaction_details transaction_details_counterparty_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.transaction_details
    ADD CONSTRAINT transaction_details_counterparty_id_fkey FOREIGN KEY (counterparty_id) REFERENCES public.counterparty(id);


--
-- Name: transaction_details transaction_details_txn_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.transaction_details
    ADD CONSTRAINT transaction_details_txn_id_fkey FOREIGN KEY (txn_id) REFERENCES public.transactions(txn_id);


--
-- Name: transactions transactions_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id);


--
-- Name: user_credit_card_association user_credit_card_association_credit_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.user_credit_card_association
    ADD CONSTRAINT user_credit_card_association_credit_card_id_fkey FOREIGN KEY (credit_card_id) REFERENCES public.credit_cards(id);


--
-- Name: user_credit_card_association user_credit_card_association_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.user_credit_card_association
    ADD CONSTRAINT user_credit_card_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: wallet_new_card_association wallet_new_card_association_credit_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallet_new_card_association
    ADD CONSTRAINT wallet_new_card_association_credit_card_id_fkey FOREIGN KEY (credit_card_id) REFERENCES public.credit_cards(id);


--
-- Name: wallet_new_card_association wallet_new_card_association_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallet_new_card_association
    ADD CONSTRAINT wallet_new_card_association_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES public.wallets(id);


--
-- Name: wallets wallets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cardmathdb
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_advance(text, pg_lsn); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_advance(text, pg_lsn) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_create(text); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_create(text) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_drop(text); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_drop(text) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_oid(text); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_oid(text) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_progress(text, boolean); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_progress(text, boolean) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_session_is_setup(); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_is_setup() TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_session_progress(boolean); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_progress(boolean) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_session_reset(); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_reset() TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_session_setup(text); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_setup(text) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_xact_reset(); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_xact_reset() TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_replication_origin_xact_setup(pg_lsn, timestamp with time zone); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_xact_setup(pg_lsn, timestamp with time zone) TO cloudsqlsuperuser;


--
-- Name: FUNCTION pg_show_replication_origin_status(OUT local_id oid, OUT external_id text, OUT remote_lsn pg_lsn, OUT local_lsn pg_lsn); Type: ACL; Schema: pg_catalog; Owner: cloudsqladmin
--

GRANT ALL ON FUNCTION pg_catalog.pg_show_replication_origin_status(OUT local_id oid, OUT external_id text, OUT remote_lsn pg_lsn, OUT local_lsn pg_lsn) TO cloudsqlsuperuser;


--
-- PostgreSQL database dump complete
--

