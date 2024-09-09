import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
def connect_to_database(database_name,port_number,database_user,database_password,host_name):
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
            user = database_user,
            password = database_password,
            host = host_name,
            port = port_number
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
load_dotenv()
DB_HOST = os.getenv("DB_HOST_NAME")
DB_PORT = os.getenv("DB_PORT_NUMBER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
def get_dataFrame_from_database():
    conn = connect_to_database(DB_NAME,DB_PORT,DB_USER,DB_PASSWORD,DB_HOST)
    if conn is not None:
        query = "SELECT * FROM xdr_data"
        xdr_data = execute_query(conn, query)

        if xdr_data is not None:
            return xdr_data
        
        conn.close()

def export_eng_exp_sat_to_psql(data):
    conn = connect_to_database(DB_NAME,DB_PORT,DB_USER,DB_PASSWORD,DB_HOST)
    try:
        cursor = conn.cursor()

        print(cursor)
        # Create the table (adjust column types as needed)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS eng_exp_sat (
            user_id serial NOT NULL PRIMARY KEY,
            MSISDN FLOAT,
            engagement_score FLOAT,
            experience_score FLOAT,
            satisfaction_score FLOAT
        )
        """
        cursor.execute(create_table_query)
        # Insert data into the table
        for index, row in data.iterrows():
            insert_query = f"""
            INSERT INTO eng_exp_sat (MSISDN, engagement_score, experience_score, satisfaction_score)
            VALUES ({row['MSISDN/Number']}, {row['engagement_score']}, {row['experience_score']}, {row['satisfaction_score']});
            """
            cursor.execute(insert_query)
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None


def fetch_data_from_database():
    conn = connect_to_database(DB_NAME,DB_PORT,DB_USER,DB_PASSWORD,DB_HOST)
    if conn is not None:
        select_query = "SELECT * FROM eng_exp_sat"
        results_data = execute_query(conn, select_query)

        if results_data is not None:
            return results_data
        
        conn.close()
