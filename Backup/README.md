### Data modeling with Postgres
Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app, specifically understanding what songs users are listening to. The data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
We have to create a database schema and ETL pipeline for this analysis.

### Data
- **Song datasets**: All json files are under data/song_data. A sample is:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

- **Log datasets**: All json files are under data/log_data. A sample subset of a file is:

```
{"artist":"Stephen Lynch","auth":"Logged In","firstName":"Jayden","gender":"M","itemInSession":0,"lastName":"Bell","length":182.85669,"level":"free","location":"Dallas-Fort Worth-Arlington, TX","method":"PUT","page":"NextSong","registration":1540991795796.0,"sessionId":829,"song":"Jim Henson's Dead","status":200,"ts":1543537327796,"userAgent":"Mozilla\/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident\/6.0)","userId":"91"}
{"artist":"Manowar","auth":"Logged In","firstName":"Jacob","gender":"M","itemInSession":0,"lastName":"Klein","length":247.562,"level":"paid","location":"Tampa-St. Petersburg-Clearwater, FL","method":"PUT","page":"NextSong","registration":1540558108796.0,"sessionId":1049,"song":"Shell Shock","status":200,"ts":1543540121796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"73"}
```

### Use of relational data modeling 
Relational data modeling is well suited for this project since the data is structured and not very big and should be flexible to support different types of ad-hoc analytical queries, including JOINS across multiple tables.

### Databse schema 
The schema used for this project is the Star Schema with a total of 5 tables.
There is one fact table containing all the measures associated to each event (user song plays) and 4 dimentional tables, each with a primary key that is being referenced from the fact table.

### Dimension Tables / Schema

**songs** - with a specific primary key
- song_id varchar PRIMARY KEY NOT NULL,
- title varchar NOT NULL,
- artist_id varchar NOT NULL,
- year int,
- duration float

**artists** - with a specific primary key
- artist_id varchar PRIMARY KEY NOT NULL,
- name varchar,
- location varchar,
- latitude float,
- longitude float


**users** - with a specific primary key
- user_id varchar PRIMARY KEY NOT NULL,
- first_name varchar,
- last_name varchar, 
- gender varchar,
- level varchar

**time** - with a specific primary key
- start_time timestamp PRIMARY KEY NOT NULL,
- hour int,
- day int,
- week int,
- month int, 
- year int,
- weekday int

### Fact Table / Schema

**songplays** - with a specific primary key, SERIAL data type used to define auto-incremented column
- songplay_id SERIAL PRIMARY KEY, 
- start_time timestamp, 
- user_id varchar, 
- level varchar, 
- song_id varchar, 
- artist_id varchar, 
- session_id int, 
- location varchar, 
- user_agent varchar

### Project Organization

Files used:
- **README.md** : READMe for project 
- **data** : data folder
- **create_tables.py** : drops and creates tables
- **sql_queries.py** : all sql queries
- **etl.ipynb** : reads and processes a single file from song_data and log_data and loads the data into tables 
- **etl.py** : reads and processes files from song_data and log_data and loads them into tables
- **test.ipynb** : used for testing


### Brief Description of updates made to SQL/Python files

**sql_queries.py** : 
- Created 5 tables with right data types, only if the tables do not exist and also specified the right primary keys. For songplays table, SERIAL data type has been used to define auto-incremented column. 
- Also defined the insert row functions for the 5 tables and specified that in case of conflict with primary key, do nothing.
- In addition, the song_select function is defined to extract song_id and artist_id based on song title, artist name and song duration in the log dataset since the song_id and artist_id are not natively defined in the log dataset

**etl.py / etl.ipynb**: 
- process_song_file function opens the specifc json file in filepath and reads into a dataframe (with one row). The row is converted to a list and then inserted into the specific table
- process_log_file opens the specifc json file in filepath and reads into a dataframe (with multiple rows). df is first filtered and the time column is converted into another dataframe time_df with multiple columns. Then, with a for loop, the rows in time_df are inserted into the time table. user_df is created by selecting specific columns from df. Then, with a for loop, the rows in user_df are inserted into the users table. For populating the songplays table an additional step is required since the artistid and songid datafields are not available in the df created from logs json file. So as we iterate through the rows of df, we call song_select function which essentially extracts artistid and songid for a given song, artist and length. Then, with a for loop, the song plays table is populated.
- process_data function recursively creates a list all_files in filepath. Then it calls either func=process_song_file or func=process_log_file for each file in all_files

**test.ipynb**
- As per project rubric, the solution dataset will only have 1 row with values for value containing ID for both songid and artistid in the fact table. Those are the only 2 values that the query in the sql_queries.py will return that are not-NONE. The rest of the rows will have NONE values for those two variables. 
- So for adequate testing and insight generation, I added the following lines in test.ipynb

- %sql SELECT count(*) FROM songs;
- %sql SELECT count(*) FROM songplays;
- %sql SELECT count(user_id), user_id FROM songplays GROUP BY user_id ORDER BY count(user_id) DESC;
- %sql SELECT * FROM songplays WHERE song_id IS NOT NULL;
- sql SELECT * FROM songplays WHERE artist_id IS NOT NULL;
- %sql SELECT * FROM songplays WHERE song_id IS NOT NULL AND artist_id IS NOT NULL ;

**How to Run the scripts**
- python3 create_tables.py
- python3 etl.py

**Additional testing results**
- Through test.ipynb, it is verified that only one row exists in songplays table with non-null values for artist_id and song_id. 
- There are 71 records in songs table and 6820 records in songplays table
- The max number of records (689) in songplays table is for user_id 49


