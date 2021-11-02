import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import configparser

def process_song_file(cur, filepath):
    """
    This funtion does:
    1. Open a song file
    2. Insert song record into the songs table
    3. Insert artist record into the artists table 

    Args:
        cur (Cursor object): sql database cursor object
        filepath (str): file location
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This funtion does:
    1. Open a log file
    2. Insert log time data records into the time table.
        - Time data is transformed into different time values prior to inserting
    3. Insert user/update records into the user table 
    4. Insert songplay records into the songplays table
        - Data from songs table and artists table are also extracted for songplay record.

    Args:
        cur (Cursor object): sql database cursor object
        filepath (str): file location
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit = "ms")
    
    # insert time data records
    time_data = [df["ts"], t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ["start_time", "hour", "day", "week", "month", "year", "weekday"]
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

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
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function does:
    1. Accesses all json files in the filepath 
    2. Apply a given function (process_song_file or process_log_file) to the json files.

    Args:
        cur (Cursor object): sql database cursor object
        conn (Connection obeject): sql database connection object
        filepath (Str): file location
        func (function): data prosessing fuction to be used
    """
    
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
    """
    This function does:
    1. Establishes connection with the sparkify database and gets cursor to it.
    2. Insert data into database
        a. From song_data
            - Insert song record into the songs table
            - Insert artist record into the artists table 
        b. From song_data
            - Insert log time data records into the time table.
            - Insert user/update records into the user table 
            - Insert songplay records into the songplays table
    3. Closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read_file(open('sql_credential.cfg'))
    host = config['SQL']['HOST_IP']
    db_name = config['SQL']['DB_NAME']
    user = config['SQL']['DB_USER']
    password = config['SQL']['DB_PASSWORD']
    credential = "host={} dbname={} user={} password={}".format(host, db_name, user, password)


    conn = psycopg2.connect(credential)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()