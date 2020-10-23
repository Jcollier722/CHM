import mysql.connector
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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

#return a list of tuples -> tuple[0] name, tuple[1] lat, tuple[2] lon
def get_locations(connection):
    
    locations=[]
    query="SELECT * FROM campus_locations"
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)
    result=cursor.fetchall()
    for row in result:
        locations.append((row['name'],row['lat'],row['lon']))

    return locations

#get the max number of cases to set threshold for heat map
def get_max_infections(connection):
    
    query = "SELECT MAX(case_count) FROM campus_locations"
    cursor=connection.cursor(dictionary=True)
    cursor.execute(query)
    result=cursor.fetchone()
    
    return(result['MAX(case_count)'])

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
    
