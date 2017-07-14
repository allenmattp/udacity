## Map Area

Seattle, WA, United States

https://www.openstreetmap.org/relation/237385
https://mapzen.com/data/metro-extracts/metro/seattle_washington/

Uncompressed, Seattle's map area is about 1.6 GB. I began by extracting a more bite-sized sample and uploading information this into the database for review. I created four separate tables, which included: 

Nodes ['id' (primary), 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
Nodes Tags ['id' (foreign), 'key', 'value', 'type']
Ways ['id' (primary), 'user', 'uid', 'version', 'changeset', 'timestamp']
Ways Tags ['id' (foreign), 'key', 'value', 'type']

Initial Review

To get a sense of the data, I began by querying information on the tags.

SELECT count(a.key) FROM (SELECT DISTINCT key FROM nodes_tags) as a;

There were 110460 node tags and 357 unique keys. The most common keys were:

| Name: Frequency |
| -------------- |
| Source: 204369 |
| housenumber: 12606 |
| city: 11132 |
| postcode: 8640 |
| created_by: 6855 |

With just the top five results inconsistencies in the data are evident. There are over 12000 nodes with housenumbers tagged, but only 11132 with a city and even fewer with postcodes. Additionally, 103 of the 357 total tags only have a single record. Many of these are perhaps excessively specific:

   (u'service:bicycle:Bicycle_Sales_and_Service', 1)
   (u'service:bicycle:diy', 1)
   (u'service:bicycle:parts', 1)
   (u'service:bicycle:pump', 1)
   (u'service:bicycle:rental', 1)
   (u'service:bicycle:repair', 1)
   (u'service:bicycle:retail', 1)
   (u'service:bicycle:sales', 1)

And could potentially be recategorized into a more general tag. Others (e.g. key: "_TMSID_" value: "568") could probably be safely discarded. The process by which these are reduced should be carefully selected however, as it would be a shame to lose useful information like key: "bearproof_storage" value: "yes".

For way tags, there were 559 unique keys from a total 332118. 179 keys had only one entry. The most common were:

| Name: Frequency |
| -------------- |
| building: 33158 |
| highway: 30965 |
| source: 29892 |
| name: 18848 |
| street: 18640 |

Looking deeper into the building category, users submitted 52 different values for the building key. The most common value was simply "yes", but they also included values as specific as "floating_home", "static_caravan" and "Tyler King's House". For some of these, the specificity is useful. For others (e.g. "garage" and "garages"), the values could be combined. 

In an attempt to clean up the building keys, I dug deeper into a few of the values. Querying

"SELECT * FROM ways_tags WHERE value='kindergarten'" I anticipated returning the row for the single building tag that appeared in earlier queries. However, multiple rows were returned! Possible keys included 'school', 'amenity' and 'building'. I felt that 'school' was most appropriate and decided to change them all accordingly:

'''
# we need the sqlite3 library to talk to the database
import sqlite3

# if we found lots of items we wanted to modify, this list can be expanded
mapping = [("kindergarten", "school")
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
'''

After completing this, I discovered that other schools actually use the 'amenity' key. I disagree, but wanted to be consistent with the rest of the data. I queried some other education and found:
	
	* universities are overwhelmingly categorized as "building", although there are a few with amenity keys.
	* schools are split between building (120) and amenities (172).

This seems to be a big point of contention. Places of worship, parking, retirement homes and apartments are just a few of the values that show up with both keys. 

Google defines an amenity as "a desirable or useful feature or facility **of** a building or place." (emphasis mine) Hence, I decided I'd switch the building "amenities" over to the actual "building" key. I used the above code, but expanded mapping to include:

'''
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
           ("publice_building", "building"),
           ("college", "building"),
           ("nursing_home", "building")
           ]
'''
This list was not comprehensive, but I didn't want to step on too many toes. If an argument could be made that the item was an amenity OF a building rather than needing to be a building itself, I tried to leave it be.

Running the above code felt ... powerful. So many changes with a single click of a button!











I began the analysis by seeing how streets were formatted.

Below is a truncated list of how the most frequently occurring labels appeared:

| Name: Frequency |
| -------------- |
| Street: 9079 |
| Northeast: 4551 |
| South: 2784 |
| Southwest: 2633 |
| Avenue: 1849 |

Looking good! Because the majority of entries used the formatting of only the first letter capitalized with no abbreviations or punctation I would seek to use this for all entries. A quick look at the less frequently occurring values confirmed, illustrated below by Avenues, confirmed that the data is not without inconsistencies:

| Name: Frequency |
| -------------- |
| Ave: 1 |
| avenue: 3 |
| AVENUE: 1 |
| Avenue: 1849 |

Using the 'initial_audit.py' program to create an informed list of values that would need changing, I created a dictionary to identify poorly formatted values and what I'd like them changed to. While not comprehensive, this would clean most of the street data.

