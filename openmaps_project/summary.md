## Map Area

Seattle, WA, United States

https://www.openstreetmap.org/relation/237385
https://mapzen.com/data/metro-extracts/metro/seattle_washington/

I selected Seattle as it has been my home for the past 5+ years. In the short time I have lived here it has been massively reshaped by tech! It seemed appropriate that, as I develop my own technical skills, I should study the area.

Uncompressed, Seattle's map area is about 1.6 GB. I used more bite-sized sample (only 166 MB) before creating the .csv files to upload into the database for review. The database includes four tables: 

Nodes ['id' (primary), 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
Nodes Tags ['id' (foreign), 'key', 'value', 'type']
Ways ['id' (primary), 'user', 'uid', 'version', 'changeset', 'timestamp']
Ways Tags ['id' (foreign), 'key', 'value', 'type']

## Initial Review

1251 different users collaborated on my chunk of Seattle's data! The most prolific was Grauer Elefant who has made 779537 contributions (definitely an outlier... number 2 is at 11818 and number 14 is under 1000). Further, 459 users have only made a single contribution. To get a sense of this data has come together into a single set, I began by querying information on the tags.

(The majority of queries performed can be viewed in the query.py file)

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

Looking deeper into the building category, users submitted 52 different values for the building key. The most common value was simply "yes", but they also included values as specific as "floating_home", "static_caravan" and "Tyler King's House". For some of these, the distinction is useful. For others (e.g. "garage" and "garages"), the values could be combined. 

In an attempt to clean up the building keys, I dug deeper into a few of the values. Querying
```SQL
"SELECT * FROM ways_tags WHERE value='kindergarten'" 
```
I anticipated returning the row for the single building tag that appeared in earlier queries. However, multiple rows were returned! Possible keys included 'school', 'amenity' and 'building'. I felt that 'school' was most appropriate and decided to change them all accordingly:

```python
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
```

After completing this, I performed a few additional queries to confirm the changes stuck and see if there were other academic buildings I could modify. In doing so I discovered that other schools actually use the 'amenity' key. I disagree with this categorization, but wanted to be consistent with the rest of the data. I queried some other education and found:
	
* universities are overwhelmingly categorized as "building", although there are a few with amenity keys.
* schools are split between building (120) and amenities (172).

This seems to be a big point of contention. Places of worship, parking, retirement homes and apartments are just a few of the values that show up with both keys. 

Google defines an amenity as "a desirable or useful feature or facility **of** a building or place." (emphasis mine) Hence, I decided I'd switch the building "amenities" over to the actual "building" key. I used the above code, but expanded mapping to include:

```python
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
```
This list was not comprehensive, but I didn't want to step on too many toes. If an argument could be made that the item was an amenity OF a building rather than needing to be a building itself, I tried to leave it be.

Running the above code felt ... powerful. So many changes with a single click of a button!

Whenever so many people collaborate on a project like this there are bound to be inconsistencies on how things are categorized. Building vs. Amenity is just one example; within these keys, there are a number of arguably equal values categorized differently. For example, public_building, community_centre and social_facility are all present in the database. How fiercely one would want to seek out these similar values is up for debate, but consistency would certainly be useful. If someone wished to, for example, explore if there was any relationship between high school graduation rates and access to community centres, overlooking data due to inconsistencies could majorly impact the study. For this reason I would argue that, in cases where the difference between different values is marginal, a strictly enforced standard is desirable. While gaining community consensus would be challenging and would then require vigiliance moderating it, the extra effort would be worthwhile.

A similar concern is one of specificity. In the dataset there exists categories for similar but (unlike the previous case) not identical items. For example, values for church, synagogue and place_of_worship all exist. An argument could be made that, in order to avoid overlooking items, these should all be combined into the more general place_of_worship. However, in these instances, I believe there is enough difference between the items that the increased division is desirable. While there's merit into combining values like hospital, doctor_office and dentist into a single catch-all category, the loss of nuance between the items outweighs whatever gains would be had.
