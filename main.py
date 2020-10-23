from flask import Flask
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from collections import defaultdict
import pandas as pd
import map_data as md
import branca.colormap as cm
import configparser
import json
app = Flask(__name__)

@app.route('/')
def index():
    #Stockon University Lat and Lon
    start_coords = (39.4920,-74.5305)
    stockton_map = folium.Map(location=start_coords, zoom_start=16)

    df = pd.read_csv('campus_locations.csv',header=0)
    stockton_map.choropleth(geo_data='stockton.geojson',
                            data=df,
                            columns=['name','count'],
                            key_on='feature.properties.name',
                            fill_color = 'OrRd'
                            )
    
    #create a colormap for legend
    #colormap = cm.LinearColormap(colors=['lightblue','green','yellow','red'], index=[0,25,50,100],vmin=0,vmax=100)
    #colormap.add_to(stockton_map)

    #feature group to store location markers
    marker_group=folium.FeatureGroup(name="Building Markers",show=True)
    stockton_map.add_child(marker_group)

    #feature group for heat data
    heat_group=folium.FeatureGroup(name="Heat Data",show=True)
    stockton_map.add_child(heat_group)
    
    #get all the known locations on campus
    locations=md.get_locations(md.get_connection())

    #drop a pin on all known buildings
    for loc in locations:
        folium.Marker(location=[loc[1],loc[2]],popup=loc[0]).add_to(marker_group)
        

    #overlay heatmap
    infections=md.get_infected_locations(md.get_connection())
    HeatMap(infections,radius=30).add_to(heat_group)

    #allow user to show or hide layers (heat and markers)
    folium.LayerControl().add_to(stockton_map)
    
    return stockton_map._repr_html_()



    

if __name__ == '__main__':
    app.run()
