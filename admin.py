import mysql.connector
import configparser
from mysql.connector import Error


def add_location(connection,name,lat,lon):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO `campus_locations` (`name`, `lat`, `lon`) VALUES (%s, %s, %s)',(name, lat,lon,))
        return("Success")
    except Exception as e:
        return (e)
