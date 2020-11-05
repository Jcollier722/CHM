import mysql.connector
import configparser
import pandas as pd
from mysql.connector import Error

#return a list of tuples -> tuple[0] name, tuple[1] lat, tuple[2] lon
def get_locations(connection):
    
    locations=[]
    query="SELECT * FROM campus_locations"
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)
    result=cursor.fetchall()
    for row in result:
        locations.append((row['name'],row['lat'],row['lon'],row['case_count']))

    return locations

#get the max number of cases to set threshold for heat map
def get_max_infections(connection):
    
    query = "SELECT MAX(case_count) FROM campus_locations"
    cursor=connection.cursor(dictionary=True)
    cursor.execute(query)
    result=cursor.fetchone()
    
    return(result['MAX(case_count)'])

def get_table_as_df(connection):
    df = pd.read_sql('SELECT * FROM campus_locations',connection)
    return df
    

#return a list of tuples containing lat lon and case count of locations that have seen cases
def get_infected_locations(connection):
    results=[]
    query = "SELECT lat,lon,case_count FROM campus_locations WHERE case_count IS NOT NULL"
    cursor=connection.cursor(dictionary=True)
    cursor.execute(query)
    result=cursor.fetchall()

    for row in result:
        results.append((((row['lat'],row['lon'],row['case_count']))))

    return results

def get_login(connection,username,password):
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM login WHERE username= %s AND password = %s", (username, password,))
    account=cursor.fetchone()
    return(account)

    

    
