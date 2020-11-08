from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_nav import Nav
from flask_nav.elements import *
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from collections import defaultdict
import pandas as pd
import map_data as md
import admin as ad
import db
import branca.colormap as cm
import configparser
import json

app = Flask(__name__)
app.secret_key='stockton'


@app.route('/heat', methods=['GET', 'POST'])
def heatmap():
    #Stockon University Lat and Lon
    start_coords = (39.4920,-74.5305)
    stockton_map = folium.Map(location=start_coords, zoom_start=16)
    
    #create a colormap for legend
    colormap = cm.LinearColormap(colors=['lightblue','green','yellow','red'], index=[0,25,50,100],vmin=0,vmax=100)
    colormap.add_to(stockton_map)

    #feature group to store location markers
    marker_group=folium.FeatureGroup(name="Building Markers",show=True)
    stockton_map.add_child(marker_group)

    #feature group for heat data
    heat_group=folium.FeatureGroup(name="View by area",show=False)
    stockton_map.add_child(heat_group)


    df = md.get_table_as_df(db.get_connection())
    folium.Choropleth(name = "View by Building",geo_data='stockton.geojson',
                            data=df,
                            columns=['name','case_count'],
                            key_on='feature.properties.name',
                            fill_color = 'OrRd'
                            ).add_to(stockton_map)
    
    #get all the known locations on campus
    locations=md.get_locations(db.get_connection())

    #drop a pin on all known buildings
    for loc in locations:
        folium.Marker(location=[loc[1],loc[2]],popup=(loc[0]+" Cases: "+str(loc[3]))).add_to(marker_group)

    #overlay heatmap
    infections=md.get_infected_locations(db.get_connection())
    HeatMap(infections,radius=30).add_to(heat_group)

    #allow user to show or hide layers (heat and markers)
    folium.LayerControl().add_to(stockton_map)
    
    return stockton_map._repr_html_()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#validate login and create session
@app.route('/adminLogin', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        login_attempt=md.get_login(db.get_connection(),request.form['username'],request.form['password'])
        if(login_attempt != None):
            if request.form['username'] != login_attempt['username'] or request.form['password'] != login_attempt['password']:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['loggedin']=True
                session['username']=login_attempt['username']
                return redirect(url_for('admin_home'))
        error = 'Invalid Credentials. Please try again.'
    return render_template('adminLogin.html', error=error)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

@app.route('/adminHome', methods=['GET', 'POST'])
def admin_home():

    #get locations for drop-down menu
    location_list=ad.get_location_list(db.get_connection())
   
    if request.method == 'POST':
        print(ad.add_location(db.get_connection(),request.form['name'],request.form['lon'],request.form['lat']))
        
    return render_template('adminHome.html',location_list=location_list)
    

if __name__ == '__main__':
    app.run()
