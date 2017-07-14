Step 1:

Using csvprep, create .csv files from sample.osm

Step 2:

Create new database using openmaps.sql and upload csv files from step 1 (note: way_nodes were discarded)

Step 3:

Use the .py files to query/update the database:

* query : most queries mentioned in summary are stored here
* buildingupdate : changes key for number of ways_tags values
* cityupdate : remove , WA from value of city keys
* bcpostupdate : formats B.C. postal codes
* uspostupdate : formats U.S. postal codes



Resources:
Relied on course notes, Stack Overflow, SQLite documentation and W3Schools