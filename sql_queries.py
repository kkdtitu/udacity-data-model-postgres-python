# DROP TABLES
# only if it exists

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLE with right data types only if the table does not exist 
# Specifies primary key, SERIAL data type used to define auto-incremented column 

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL PRIMARY KEY, 
start_time timestamp REFERENCES time(start_time), 
user_id varchar REFERENCES users(user_id), 
level varchar, 
song_id varchar REFERENCES songs(song_id), 
artist_id varchar REFERENCES artists(artist_id), 
session_id int, 
location varchar, 
user_agent varchar,
UNIQUE (start_time, user_id, session_id))
""")

# CREATE TABLE with right data types only if the table does not exist 
# Specifies primary key

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id varchar PRIMARY KEY NOT NULL,
first_name varchar,
last_name varchar, 
gender varchar,
level varchar
)
""")

# CREATE TABLES with right data types only if the table does not exist 
# Specifies primary key

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar PRIMARY KEY NOT NULL,
title varchar NOT NULL,
artist_id varchar NOT NULL,
year int,
duration float
)
""")

# CREATE TABLES with right data types only if the table does not exist 
# Specifies primary key

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar PRIMARY KEY NOT NULL,
name varchar,
location varchar,
latitude float,
longitude float
)
""")

# CREATE TABLES with right data types only if the table does not exist 
# Specifies primary key

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time timestamp PRIMARY KEY NOT NULL,
hour int,
day int,
week int,
month int, 
year int,
weekday int
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays(
start_time, 
user_id, 
level, 
song_id, 
artist_id, 
session_id, 
location, 
user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

# INSERT RECORDS
#Also specifies that in case of conflict with primary key, do nothing

user_table_insert = ("""
INSERT INTO users (
user_id,
first_name,
last_name, 
gender,
level
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) 
DO UPDATE SET level = excluded.level
""")

# INSERT RECORDS
#Also specifies that in case of conflict with primary key, do nothing

song_table_insert = ("""
INSERT INTO songs (
song_id,
title,
artist_id,
year,
duration) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO NOTHING
""")

# INSERT RECORDS
#Also specifies that in case of conflict with primary key, do nothing

artist_table_insert = ("""
INSERT INTO artists (
artist_id,
name,
location,
latitude,
longitude
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING
""")

# INSERT RECORDS
#Also specifies that in case of conflict with primary key, do nothing

time_table_insert = ("""
INSERT INTO time (
start_time,
hour,
day,
week,
month, 
year,
weekday
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS
#This is required to extract song_id and artist_id based on song title, artist name and song duration

song_select = ("""
SELECT songs.song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# QUERY LISTS to create and drop a list of tables

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]