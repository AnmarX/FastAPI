CREATE TABLE IF NOT EXISTS public.users (
    id serial NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    username VARCHAR(50),
    email VARCHAR(255),
    disables boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);
