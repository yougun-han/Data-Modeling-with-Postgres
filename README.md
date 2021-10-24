# Data-Modeling-with-Postgres

## Table of Contents
1. [Description](#Description)
2. [Schema Design](#schemadesign)
3. [Getting Started](#gettingstarted)
    1. [Software and Libraries](#libraries)
    2. [File Description](#FileDescription)
    3. [Run Program](#RunProgram)
3. [Output(WebApp)](#Output)
4. [Author](#Author)
5. [Acknowledgements](#Acknowledgements)

## Description <a name="Description"></a>
This project is completed as a part of Udacity Data Engineering Nanodegree Program.

The goal of the project is to design data warehouse for a fictitous music stream company, Sparkify and implement it in a Postgres (local) SQL server. 



## Schema design and ETL pipeline  <a name="Description"></a>
The new database is designed such that song play data can be easily analysed by song, user, artist, and time. One fact table and four dimension tables are designed as detailed below:

### Fact Table
 - songplays - records in log data associated with song plays i.e. records with page NextSong
    * Columns : songplay_id (Primary Key), start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
 - users - users in the app
    * Columns : user_id (Primary Key), first_name, last_name, gender, level
 - songs - songs in music database
    * Columns : song_id (Primary Key), title, artist_id, year, duration
 - artists - artists in music database
    * Columns : artist_id (Primary Key), name, location, latitude, longitude
 - time - timestamps of records in songplays broken down into specific units
    * Columns : start_time (Primary Key), hour, day, week, month, year, weekday
 
The primary keys of four dimension tables appear in the fact table as foreign keys. This allows analysts to join fact tables with dimension tables and to perform efficient queries.

Data for songs and artists tables are extracted from song dataset. Data for time and users are extracted from log dataset. Finally, data for songplay table is extracted from songs table, artists table and log data set. During the extraction, if duplicated primary keys are detected in user data, user's first name, last name, and level overwrite the existing record. This reflects that user may change their first name, ast name or subscription level.

## Getting Started <a name="gettingstarted"></a>
### File Description <a name="FileDescription"></a>
<pre>
- Data-Modeling-with-Postgres
|- sql_queries.py   # It ontains sql queries, and is imported by "create_tables.py" and "etl.py"
|- etl.ipynb        # development and test file for "create_tables.py" and "etl.py"
|- test.ipynb       # development test file. It can be used for testing while developing etl.ipynb 
|- data
|   |- log_data     # It contains users log data
|   |- song_data    # It contains song data
</pre>

### Run Program <a name="RunProgram"></a>
1. Run a local postgres sql server.
1. Fill up the sql credential information in sql_credential.cfg.
2. Copy song json files into .../data/song_data/
3. Copy log json files into .../data/log_data/
5. Run create_tables.py
6. Run etl.py
