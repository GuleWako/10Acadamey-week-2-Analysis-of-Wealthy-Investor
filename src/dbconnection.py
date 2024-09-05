import psycopg2
import pandas as pd

def connect_to_database(database_name):
    """
    Connects to a PostgreSQL database and returns a connection object.

    Args:
        database_name (str): The name of the database.
        user (str): The username for the database.
        password (str): The password for the database.
        host (str): The hostname of the database server.
        port (int): The port number of the database server.

    Returns:
        psycopg2.connect: A connection object to the database.
    """

    try:
        conn = psycopg2.connect(
            database= database_name,
            user = "postgres",
            password = "admin",
            host = "localhost",
            port = 5432
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(conn, query):
    """
    Executes a SQL query on a given connection and returns the results as a pandas DataFrame.

    Args:
        conn (psycopg2.connect): A connection object to the database.
        query (str): The SQL query to execute.

    Returns:
        pandas.DataFrame: A DataFrame containing the query results.
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
        return df
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None

def get_dataFrame_from_database():
    database_name = "tellcom_db"
    conn = connect_to_database(database_name)
    if conn is not None:
        query = "SELECT * FROM xdr_data"
        xdr_data = execute_query(conn, query)

        if xdr_data is not None:
            return xdr_data
        
        conn.close()
