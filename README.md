# Data-Modeling-with-Postgres

## Table of Contents
1. [Description](#Description)
    1. [Introduction](#Introduction)
    2. [Raw Dat](#RawData)
2. [Schema Design](#SchemaDesign)
    1. [Fact Table](#FactTable)
    2. [Dimension Table](#DimensionTable)
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

### Introduction <a name="Introduction"></a>
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app and provide a personalised experience to the users. One of the examples would be building a music recommendation system based on user's preference like a favourite genre and/or artist. This will increase the quality of user experience and potentially reduce the churn rate. Additionally understanding the general trend of the music industry would be beneficial to the company in a way that the app service can provide the users additional recommendation according to the up-to-date music trend.   

User's music preference information can be manually specified by users in their account. However, users may not provide their specific musical taste and furthermore, this information can be easily outdated. People move on and change their style and fondness and won't bother to update this information in their account. Also, it is not easy for the company to manually catch up on what is happening in the music industry. The better approach would be to figure out what users want and what is hot based on the user's behaviour. What users listen tells what users want and trend. For this purpose, 

Sparkify has been collecting on songs and user activity in their music streaming app, but currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. Sparkfiy needs to develop a database that is optimised for the user's song play analysis. The new database should provide analyst easy access to summary data with simple querries. For example, song play summary data by users, songs, artist, and play time should be easy to query. With such a database, Sparkify can find what songs are popular, who is the hottest singers now, who is listening to what, when, and where.

As a data engineer, I created a database schema and ETL pipeline to optimize queries on song play analysis. 

### Raw Data <a name="RawData"></a>





## Schema Design <a name="SchemaDesign"></a>
The new database is designed such that song play data can be easily analysed by song, user, artist, and time. One fact table and four dimension tables are designed as detailed below:

### Fact Table <a name="FactTable"></a>
 - songplays - records in log data associated with song plays i.e. records with page NextSong
    * Columns : songplay_id (Primary Key), start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables <a name="DimensionTable"></a>
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
