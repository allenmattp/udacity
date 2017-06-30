INTRODUCTION
This is my version of the final project for Udacity's Intro to Relational Databases course.

This project is written in Python and uses a PostgreSQL database to track players and matches in a tournament.

The tournament uses the Swiss system for pairing players in each round: players are not eliminated, and in each round players are matched with another player who has the same number of wins (or as close as possible).

The database schema is defined in tournament.sql and the code for using the database in tournament.py

The code only supports a single tournament at a time and assumes an even number of players.

FUNCTIONS IN TOURNAMENT.PY
registerPlayer(name)
Adds a player to the tournament by putting an entry in the database. Players can share names, but each entrant will have a unique id.

countPlayers()
Returns the number of currently registered players.

deletePlayers()
Clear out all the player records from the database.

reportMatch(winner, loser)
Stores the outcome of a single match between two players in the database.

deleteMatches()
Clear out all the match records from the database.

playerStandings()
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

swissPairings()
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system.