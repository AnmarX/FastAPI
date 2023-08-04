CREATE TABLE IF NOT EXISTS public.users (
    id serial NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    disables boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);
