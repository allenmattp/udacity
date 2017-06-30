-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( id SERIAL primary key,
                      name TEXT NOT NULL,
                      win INT,
                      matches INT);

CREATE TABLE matches ( match_id SERIAL primary key,
                      winner INT references players(id),
                      loser INT references players(id));