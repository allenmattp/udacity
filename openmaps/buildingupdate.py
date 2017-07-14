# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 18:36:36 2017

@author: Wizard
"""

import sqlite3

mapping = [("kindergarten", "building"),
           ("school", "building"),
           ("university", "building"),
           ("hospital", "building"),
           ("fire_station", "building"),
           ("cinema", "building"),
           ("place_of_worship", "building"),
           ("police", "building"),
           ("courthouse", "building"),
           ("dentist", "building"),
           ("post_office", "building"),
           ("townhall", "building"),
           ("bus_station", "building"),
           ("apartments", "building"),
           ("veterinary", "building"),
           ("social_facility", "building"),
           ("community_centre", "building"),
           ("Furniture Store", "building"),
           ("public_building", "building"),
           ("college", "building"),
           ("nursing_home", "building")
           ]

# this function is superfluous, but it's nice to see the before/after
def ask_question(query, key):
    db = sqlite3.connect("openmaps.db")
    c = db.cursor()
    c.execute(query, [key])
    rows = c.fetchall()
    return rows
    db.close()

# takes in a query as its order and completes the query using the given key
def give_order(order, key):
    db = sqlite3.connect("openmaps.db")
    c = db.cursor()
    c.execute(order, [key])
    db.commit()
    rows = c.fetchall()
    return rows
    db.close()

#iterates through tuples in mapping. print statements are just for peace of mind.
for key, value in mapping:
    print '* * * BEFORE * * *:'
    print ask_question('SELECT * FROM ways_tags WHERE value=?', key)
    rows = give_order('UPDATE ways_tags SET key = "'+value+'" WHERE value=?', key)
    print '* * * AFTER * * *:'
    print ask_question('SELECT * FROM ways_tags WHERE value=?', key)
