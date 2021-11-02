import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import configparser

def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # read sql access credential information
    config = configparser.ConfigParser()
    config.read_file(open('sql_credential.cfg'))
    host = config['SQL']['HOST_IP']
    db_name = config['SQL']['DB_NAME']
    user = config['SQL']['DB_USER']
    password = config['SQL']['DB_PASSWORD']
    credential = "host={} dbname={} user={} password={}".format(host, db_name, user, password)


    # connect to default database
    conn = psycopg2.connect(credential)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.

    Args:
        cur (Cursor object): sql database cursor object
        conn (Connection obeject): sql database connection object

    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 

    Args:
        cur (Cursor object): sql database cursor object
        conn (Connection obeject): sql database connection object
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - At the last step, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()