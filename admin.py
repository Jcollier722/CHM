import mysql.connector
import configparser
from mysql.connector import Error


#add a location to the db
def add_location(connection,name,lat,lon):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO `campus_locations` (`name`, `lat`, `lon`) VALUES (%s, %s, %s)',(name, lat,lon,))
        return("Success")
    except Exception as e:
        return (e)

def get_location_list(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT name FROM campus_locations')
        return (cursor.fetchall())
    except Exception as e:
        returm (e)

