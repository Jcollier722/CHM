import mysql.connector
import configparser
import pandas as pd
import db as db
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

def add_case(location):
    connection = db.get_connection()
    #get current case count, increment by one
    cases=get_case_count(connection,location[0])

    if(location[1]=="high risk"):
        cases = cases + 2
    if(location[1]=="medium risk"):
        cases = cases + 1

    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('UPDATE campus_locations SET case_count=%s WHERE name =%s',(cases,location[0],))
        connection.commit()
        return("Added case to "+str(location[0]))
    except Exception as e:
        return (e)

def get_case_count(connection,location):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT case_count FROM campus_locations WHERE name = %s',(location,))
        count = cursor.fetchone()
        connection.commit()
        return(int(count['case_count']))
    except Exception as e:
        return (e)
    

def get_login(connection,username,password):
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM login WHERE username= %s AND password = %s", (username, password,))
    account=cursor.fetchone()
    return(account)

    

    
