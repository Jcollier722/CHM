import mysql.connector
import configparser
import traceback
import const
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
    risk_score = 0
    risk_factor = "low"
    
    #inner class to represent a person's demo graphics
    #representating a person as an object makes the risk score easier to understand
    class __person__:
        def __init__(self,gender,age,feels_sick,close_contact,pre_exs,sym_list):
            self.gender = gender
            self.age    =age
            self.feels_sick = feels_sick
            self.close_contact=close_contact
            self.pre_exs=pre_exs
            self.sym_list=sym_list

    #build the person object    
    this_person = __person__(user_answers[0],user_answers[1],
                             user_answers[2],user_answers[3],
                             user_answers[4],user_answers[5:])
                             
    #men are more at risk than women
    if(this_person.gender == "Male"):
        risk_score = risk_score + 1

    #if user feels ill add risk points
    if(this_person.feels_sick=="ill"):
        risk_score = risk_score + 1

    #if user has been around confirmed case add risk
    if(this_person.close_contact == "cc"):
        risk_score = risk_score + 2

    #if user has pre-exst condition add points
    if(this_person.close_contact == "pre_exs"):
        risk_score = risk_score + 2
    
    #add age risk factor (lookup from dict)
    risk_score=risk_score+(const.age_risk_dict[this_person.age])

    #if user has new symtomps, match them with potenial cluster
    if(len(this_person.sym_list)!=0):
        risk_score=risk_score + (cluster_analysis(connection,this_person.sym_list))
    
    #determine risk factor based on score
    if(0 <= risk_score <= 6):
        risk_factor = "low"
    elif(6 <= risk_score <= 11):
        risk_factor = "medium"
    elif(11 <= risk_score <= 20):
        risk_factor = "high"

    #return tuple of risk score and factor
    return ((risk_score,risk_factor))

def cluster_analysis(connection, user_answers):
    low_risk_threshold = 0.20
    medium_risk_threshold = 0.40
    high_risk_threshold = 0.60
    low_risk = False
    medium_risk=False
    high_risk=False
    cluster_list = get_cluster_list(connection)
    cluster_dict = get_clusters(connection)

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
        return 3
    if(medium_risk):
        return 2
    if(low_risk):
        return 0
    
def get_sym_for_cluster(cluster,s_dict):
    sym_list=[]
    for entry in s_dict:
        #print(cluster)
        if(entry['cluster_id']==cluster['cluster_id']):
            sym_list.append(entry['name'])

    return sym_list
    
