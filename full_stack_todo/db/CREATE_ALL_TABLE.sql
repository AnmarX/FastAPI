CREATE TABLE IF NOT EXISTS public.users (
    user_id serial NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    disables boolean
    -- CONSTRAINT users_pkey PRIMARY KEY (user_id)
    -- CONSTRAINT location_id FOREIGN KEY (location_id) REFERENCES public.location (location_id)
);


CREATE TABLE IF NOT EXISTS public.todo (
    todo_id serial NOT NULL PRIMARY KEY,
    user_id int ,
    all_todos VARCHAR(255) NOT NULL,
    CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users (user_id)
);


-- CREATE TABLE IF NOT EXISTS public.todo (
--     todo_id serial NOT NULL PRIMARY KEY,
--     user_id int,
--     all_todos TEXT NOT NULL,
--     CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users (user_id)
-- );

