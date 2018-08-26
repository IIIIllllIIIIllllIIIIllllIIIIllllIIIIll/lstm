CREATE TABLE IF NOT EXISTS cards (
    uuid text PRIMARY KEY,
    stage int,
    due text,
    -- 0: training, 1: lapsed, 2: regular
    type int,
    ease int,
    last text,
    front text NOT NULL,
    back text NOT NULL
);
