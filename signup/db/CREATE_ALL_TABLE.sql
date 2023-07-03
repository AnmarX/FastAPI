CREATE TABLE IF NOT EXISTS public.users (
    id serial NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    username VARCHAR(50),
    email VARCHAR(255),
    CONSTRAINT users_pkey PRIMARY KEY (id)
);
