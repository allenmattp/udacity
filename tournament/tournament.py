#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, bleach

DBNAME = "tournament"

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dbname=DBNAME)


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    c.execute("UPDATE players SET win = 0, matches = 0;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    # c.execute("UPDATE players SET win = Null, matches = Null;")
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    #c.execute("SELECT COUNT ( DISTINCT id ) AS participants FROM players;")
    c.execute("SELECT COUNT(*) FROM players;")
    count = c.fetchone()
    db.close()
    return int(count[0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name, win, matches) VALUES (%s, 0, 0)", (bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT id, name, win, matches FROM players ORDER BY win;")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES (%s, %s)", (bleach.clean(winner), bleach.clean(loser),))
    c.execute("UPDATE players SET win = win + 1, matches = matches + 1 WHERE id = %s", (bleach.clean(winner),))
    c.execute("UPDATE players SET matches = matches + 1 WHERE id = %s", (bleach.clean(loser),))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    matches = []
    pairs = ()
    for player in standings:
        if len(pairs)<1:
            pairs += player[0:2]
        else:
            pairs += player[0:2]
            matches.append(pairs)
            pairs = ()
    return matches