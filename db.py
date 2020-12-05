import mysql.connector
import configparser
from mysql.connector import Error

#return connection to sql
def create_connection(host_name, user_name, user_password,db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db
        )
        #print("connected to db")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

#Function to run SQL query. Pass function from map_data.py return results of util function.   
def get_connection():
    #get sql credentials from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    host=config.get('mysql','host')
    username=config.get('mysql','username')
    password=config.get('mysql','password')
    database=config.get('mysql','db')

    #connect to database
    connection=create_connection(host,username,password,database)

    return(connection)

