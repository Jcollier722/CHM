import mysql.connector
import configparser
import traceback
from mysql.connector import Error


#add a location to the db
def add_location(connection,name,lat,lon):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO `campus_locations` (`name`, `lat`, `lon`) VALUES (%s, %s, %s)',(name, lat,lon,))
        connection.commit()
        return("Success add")
    except Exception as e:
        return (e)
    
#remove location from db
def remove_location(connection,name):
    try:
        cursor=connection.cursor(dictionary=True)
        cursor.execute('DELETE FROM `campus_locations` WHERE name = %s',(name,))
        connection.commit()
        return("Success remove")
    except Exception as e:
        return (e)
    
#get list of locations as a dictonary        
def get_location_list(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT name FROM campus_locations')
        return (cursor.fetchall())
    except Exception as e:
        return (e)

#add a new admin
def add_user(connection,username,password):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO `login`(`username`, `password`) VALUES (%s,%s)',(username,password,))
        connection.commit()
        return("Success add user")
    except Exception as e:
        return (traceback.print_exc())


        
