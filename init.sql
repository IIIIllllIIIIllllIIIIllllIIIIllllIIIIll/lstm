CREATE TABLE IF NOT EXISTS cards (
    uuid text PRIMARY KEY,
    stage int,
    due text,
    training_mode boolean,
    graduating_interval int,
    ease int,
    last text,
    front text NOT NULL,
    back text NOT NULL
);
