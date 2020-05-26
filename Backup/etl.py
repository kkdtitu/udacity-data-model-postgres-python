import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

'''
- Goes through the list of all song files and log files and updates the 5 tables
'''

def process_song_file(cur, filepath):
    '''
    This function opens the specifc json file in filepath and reads into a dataframe (with one row)
    The row is converted to a list and then inserted into the specific table
    '''
    
    # open song file
    df = pd.read_json(filepath, lines=True)
    df1 = df[['song_id', 'title', 'artist_id', 'year', 'duration']]

    # insert song record
    song_data = df1.values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    df1 = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = df1.values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    This function opens the specifc json file in filepath and reads into a dataframe (with multiple rows)
    
    df is first filtered and the time column is converted into another dataframe time_df with multiple 
    columns. Then, with a for loop, the rows in time_df are inserted into the time table.
    
    user_df is created by selecting specific columns from df. 
    Then, with a for loop, the rows in user_df are inserted into the users table.
    
    For populating the songplays table an additional step is required since the artistid and songid
    datafields are not available in the df created from logs josn file. 
    So as we iterate through the rows of df, we call song_select function which essentially 
    extracts artistid and songid for a given song, artist and length.
    Then, with a for loop, the song plays table is populated.
    
    '''
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'].str.contains("NextSong")]

    # convert timestamp column to datetime
    df1 = df[['ts']]
    t = pd.to_datetime(df1['ts'], unit='ms')
    
    # insert time data records
    time_data = [t, \
             t.dt.hour, \
             t.dt.day, \
             t.dt.week, \
             t.dt.month, \
             t.dt.year, \
             t.dt.dayofweek]
    column_labels = ['ts', 'hour', 'day', 'week', 'month', 'year', 'dayofweek']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, \
                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    This function recursively creates a list all_files in filepath
    Then it calls either func=process_song_file or func=process_log_file for each file in all_files
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()