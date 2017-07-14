# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:13:51 2017

@author: Wizard
"""

import sqlite3
import re

find_five = re.compile(r'(\d{5})')

queries = {
        "a": "SELECT * FROM nodes_tags WHERE key='postcode';"}

# query the database and return results as rows
def ask_question(query):
    db = sqlite3.connect("openmaps.db")
    c = db.cursor()
    c.execute(query)
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

# store results of query in [values]
def compiler(query):
    values = []
    for row in ask_question(query):
        values.append(row)
    return values

# for US postal codes remove all but 5 digit zip
def modifier(query):
    original = compiler(query)
    for e in original:
        if len(e[2]) > 5:
            zip = find_five.search(e[2])
            if zip:
                give_order("UPDATE nodes_tags SET value='"+zip.group(1)+"' WHERE key ='"+e[1]+"' and id=?", e[0])

modifier(queries['a'])
