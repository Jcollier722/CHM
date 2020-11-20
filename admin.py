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

#get clusters
def get_cluster_list(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT DISTINCT cluster_id FROM symptom')
        return (cursor.fetchall())
    except Exception as e:
        return (e)

#get clusters
def get_sym_list(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT DISTINCT name FROM symptom')
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

def add_sym(connection,sym,cluster):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO `symptom`(`name`, `cluster_id`) VALUES (%s,%s)',(sym,cluster,))
        connection.commit()
        return("Success add sym")
    except Exception as e:
        return (traceback.print_exc())
    
def rem_sym(connection,sym):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('DELETE FROM `symptom` WHERE name = %s',(sym,))
        connection.commit()
        return("Success rem sym")
    except Exception as e:
        return (traceback.print_exc())
    


        
