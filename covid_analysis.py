import mysql.connector
import configparser
import traceback
from mysql.connector import Error

class cluster:
    def __init__(self,c_id,sym_list):
        self.c_id = c_id
        self.sym_list=sym_list

#get unique cluster
def get_clusters(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT cluster_id,name FROM symptom')
        return (cursor.fetchall())
    except Exception as e:
        return (e)
    
#get unique 
def get_cluster_list(connection):
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT DISTINCT cluster_id FROM symptom')
        return (cursor.fetchall())
    except Exception as e:
        return (e)
    

def process_answers(connection,user_answers):
    low_risk_threshold = 0.20
    medium_risk_threshold = 0.40
    high_risk_threshold = 0.60

    low_risk = False
    medium_risk=False
    high_risk=False
    
    cluster_list = get_cluster_list(connection)
    cluster_dict = get_clusters(connection)

    #get all symompts for cluster 1
    #compare
    
    for cluster in cluster_list:
        matches=0
        cluster_syms = get_sym_for_cluster(cluster,cluster_dict)
        for answer in user_answers:
            if(answer in cluster_syms):
                matches = matches +1

        match_percent=(matches/len(cluster_syms))

        if((match_percent>0.0) and (match_percent<= low_risk_threshold)):
            low_risk=True

        if((match_percent>low_risk_threshold) and (match_percent<= high_risk_threshold)):
            medium_risk=True
            
        if((match_percent>=high_risk_threshold)):
            high_risk=True
        
    if(high_risk):
        return "high"
    if(medium_risk):
        return "medium"
    if(low_risk):
        return "low"

            
def get_sym_for_cluster(cluster,s_dict):
    sym_list=[]
    for entry in s_dict:
        #print(cluster)
        if(entry['cluster_id']==cluster['cluster_id']):
            sym_list.append(entry['name'])

    return sym_list
    
