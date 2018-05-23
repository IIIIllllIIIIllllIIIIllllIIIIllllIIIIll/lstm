CREATE TABLE IF NOT EXISTS cards (
    due text,
    is_new boolean,
    graduating_interval int,
    ease int,
    last text,
    front text NOT NULL,
    back text NOT NULL
);
