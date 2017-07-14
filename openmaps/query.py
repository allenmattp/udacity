# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:06:58 2017

@author: Wizard
"""

import sqlite3

'''
QUERY KEY:
    a : Unique key count for nodes_tags
    b : Unique key count for ways_tags
    c : Count of each key for nodes_tags
    d : Count of each key for ways_tags
    e : Count of rows for nodes
    f : Count of rows for ways
    g : Database stats
    h : Unique users
    i : Count of unique users
    ii: Count of users who have made a single contribution
    j : Unique values and their count where ways tagged as building
    k : Count of unique values for ways tagged as buildings
    l : Count number of keys in nodes_tags where only one record exists
    m : Count number of keys in ways_tags where only one record exists
    n : Count of different cities in nodes_tags
    o : Count of different postcodes in node_tags
    
'''

queries = {
        "a": "SELECT count(a.key) FROM (SELECT DISTINCT key FROM nodes_tags) as a;",
        "b": "SELECT count(a.key) FROM (SELECT DISTINCT key FROM ways_tags) as a;",
        "c": "SELECT key, count(key) as num FROM nodes_tags GROUP BY key ORDER BY num DESC;",
        "d": "SELECT key, count(key) as num FROM ways_tags GROUP BY key ORDER BY num DESC;",
        "e": "SELECT count(*) FROM nodes;",
        "f": "SELECT count(*) FROM ways;",
        "g": "pragma stats;",
        "h": "SELECT user, uid, count(*) as num FROM nodes UNION SELECT user, uid, count(*) FROM ways GROUP BY uid ORDER BY num ;",
        "i": "SELECT count(agg.uid) FROM (SELECT user, uid, count(*) as num FROM nodes UNION SELECT user, uid, count(*) FROM ways GROUP BY uid ORDER BY uid) as agg;",
        "ii": "SELECT count(agg.uid) FROM (SELECT user, uid, count(*) as num FROM nodes UNION SELECT user, uid, count(*) FROM ways GROUP BY uid ORDER BY uid) as agg GROUP BY agg.num HAVING agg.num = 1;",
        "j": "SELECT build.id, build.value, count(build.value) as num FROM (SELECT id, value FROM ways_tags WHERE key='building')as build GROUP BY build.value ORDER BY num DESC;",
        "k": "SELECT count(build.value) as num FROM (SELECT DISTINCT value FROM ways_tags WHERE key='building')as build;",
        "l": "SELECT count(one.num) as num FROM (SELECT count(key) as num FROM nodes_tags GROUP BY key having num = 1) as one;",
        "m": "SELECT count(one.num) as num FROM (SELECT count(key) as num FROM ways_tags GROUP BY key having num = 1) as one;",
        "n": "SELECT value, count(key) as num FROM nodes_tags WHERE key='city' GROUP BY value ORDER BY num DESC;",
        "o": "SELECT value, count(key) as num FROM nodes_tags WHERE key='postcode' GROUP BY value ORDER BY num DESC;"
                          }


def ask_question(query):
    db = sqlite3.connect("openmaps.db")
    c = db.cursor()
    c.execute(query)
    rows = c.fetchall()
    return rows
    db.close()

# Plug in a pre-written query from above or write your own
print
print "QUERY RESULTS:"
for row in ask_question(queries["o"]):
  print "  ", row

