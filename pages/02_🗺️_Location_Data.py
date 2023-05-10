import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page
# for choropleth graph
import geopandas as gpd
import plotly.express as px
import json
from datetime import datetime



# Sets browser tab information
st.set_page_config(page_title="NDD - Location Data",
                   page_icon="🗺️", layout="wide")

add_logo("images/lrw-color.png")

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stButton>button {
              position: fixed;
              bottom: 20px;
              right: 20px;
              z-index: 1;
              padding: 10px;
              background-color: gray;
            }
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)
# Adds title to top of page
st.title("🗺️ Disaster Locations Dashboard")
st.markdown("This is an interactive scatter map of disasters in the United States.  &nbsp;Hovering over a marked location will show more details.")
st.markdown("##")

@st.cache_data
def get_data():
     shapefile = gpd.read_file('data/cb_2018_us_county_20m.shp')
     crop_dec = pd.read_excel('data/crop-year-2014-disaster-declarations-1.xls')
     df_main = pd.read_csv('data/storm_details_whole_nums.csv')
     df_main = df_main[df_main['BEGIN_YEARMONTH'] > 201000]

     return [shapefile, crop_dec, df_main]

df_files = get_data()

@st.cache_data

def cluster_map(df_main):
  cluster = px.scatter_mapbox(df_main, lat='BEGIN_LAT', lon='BEGIN_LON', zoom=2.5, center=dict(lat=39.8, lon=-98.5))
  cluster.update_traces(cluster=dict(enabled=True))

  return cluster

# --- CHOROPLETH GRAPH ---

crop_dec = df_files[1].rename(columns = {
                        'FIPS': 'fips'
                        ,'Designation Number': 'designation number'
                        ,'DROUGHT': 'drought'
                        ,'FLOOD, Flash flooding': 'flash flooding'
                        ,'Excessive rain, moisture, humidity': 'rain'
                        ,'Severe Storms, thunderstorms': 'severe storms'
                        ,'Ground Saturation\nStanding Water': 'waterlogged'
                        ,'Hail': 'hail'
                        ,'Wind, High Winds': 'high wind'
                        ,'Fire, Wildfire': 'fire'
                        ,'Heat, Excessive heat\nHigh temp. (incl. low humidity)': 'heatwave'
                        ,'Winter Storms, Ice Storms, Snow, Blizzard': 'snow'
                        ,'Frost, FREEZE': 'frost'
                        ,'Hurricanes, Typhoons, Tropical Storms': 'hurricane'
                        ,'Tornadoes': 'tornado'
                        ,'Volcano': 'volcano'
                        ,'Mudslides, Debris Flows, Landslides': 'landslide'
                        ,'Heavy Surf': 'heavy surf'
                        ,'Ice Jams': 'ice jam'
                        ,'Insects': 'insects'
                        ,'Tidal Surges': 'tidal surge'
                        ,'Cold, wet weather': 'cold and wet'
                        ,'Cool/Cold, Below-normal Temperatures': 'cold'
                        ,'Lightning': 'lightning'
                        ,'Disease': 'disease'})

df_files[0]['GEOID'] = df_files[0]['GEOID'].astype(str)
crop_dec['fips'] = crop_dec['fips'].astype(str)
crop_dec['fips'] = [x if len(x) == 5 else "0"+x for x in crop_dec['fips']]

shapeJoin = crop_dec.merge(df_files[0], right_on = 'GEOID', left_on = 'fips')

# Set custom color scale based on range of drought values
#scale = [[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,0)']]


# Convert the geometry column to a GeoSeries
geometry = gpd.GeoSeries(shapeJoin['geometry'])
# Convert the GeoSeries to JSON format
geojson = json.loads(geometry.to_json())

def ch_graph(sel, scale, df_main):
  # Load the shapefile using geopandas


  # --- Selector for Choropleth Graph ---
    # currently "hardcoded" for columns 5 through 28
  # sel = st.selectbox('Selector for Choropleth Graph', shapeJoin.columns[5:28], help='Select the incident type you would like to see on the map. The darker the county, the more of selected incidents in that county. If you selected "drought", the county with the most droughts will appear darkest.')

  # Filter the shapeJoin dataframe based on the selected incident type
  shapeJoin_filtered = shapeJoin[shapeJoin[sel] == 1]
  # Use Plotly Express to create the choropleth graph
  fig_ch = px.choropleth_mapbox(shapeJoin_filtered,
                      title='Choropleth Graph - Work in Progress',
                      geojson=geojson,
                      locations=shapeJoin_filtered.index,
                      animation_frame=shapeJoin_filtered['Begin Date'].dt.strftime('%B %Y'),
                      color=sel,
                      opacity=0.2,
                      hover_name='County',
                      hover_data={
                        sel: False,
                        'State': True,
                        'fips': True,
                        #'Begin Date': True,
                        #'End Date': True,
                      },
                      center=dict(lat=39.8, lon=-98.5),
                      zoom=3.0,
                      height=800,
                      mapbox_style="carto-positron",
                      color_continuous_scale=scale,
                      color_continuous_midpoint=0.5,
                      labels={sel: sel.capitalize()})
  fig_ch.add_scattermapbox(lat = df_main['BEGIN_LAT'],
                        lon = df_main['BEGIN_LON'],
                        mode = 'markers+text',
                        text = 'example',  #a list of strings, one  for each geographical position  (lon, lat)
                        below='',
                        marker_size=3,
                        marker_color='rgb(235, 0, 100)')



  #timestamp = datetime.strptime('2013-10-01 00:00:00', '%Y-%m-%d %H:%M:%S')
#month_year = timestamp.strftime('%B %Y')

  # fig_ch = px.choropleth(shapeJoin_filtered,
  #             locations = shapeJoin_filtered.index,
  #             color=sel,
  #             animation_frame= shapeJoin_filtered['Begin Date'].dt.strftime('%B %Y'),
  #             color_continuous_scale="Inferno",
  #             locationmode='USA-states',
  #             scope="usa",
  #             range_color=(0, 20),
  #             title='Test',
  #             height=600
  #            )


  return fig_ch

# Function to return Choropleth Graph color
def getScale(sel):
  if sel == "drought" or sel == "landslide":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(255, 215, 0)']]
  elif sel == "flash flooding" or sel == "severe storms" or sel == "rain" or sel == "waterlogged" or sel == "hail" or sel == "cold and wet":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(0, 255, 0)']]
  elif sel == "fire" or sel == "heatwave" or sel == "volcano":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']]
  elif sel == "frost" or sel == "snow" or sel == "ice jam" or sel == "cold":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(135, 206, 235)']]
  elif sel == "hurricane" or sel == "heavy surf" or sel == "tidal surge":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(0, 0, 255)']]
  elif sel == "high wind" or sel == "tornado":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(128, 128, 128)']]
  elif sel == "lightning":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(255, 255, 0)']]
  elif sel == "insects":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(255, 204, 0)']]
  elif sel == "disease":
     return [[0, 'rgb(255,255,255)'], [1, 'rgb(204, 102, 0)']]

def graphs(df_main):
  askBot = st.button("🤖 Ask DisasterBot", use_container_width=False)
  if askBot:
    switch_page('disasterbot')
  # Creates a container on the page and displays the map
  cluster_cont = st.container()
  choro_cont = st.container()
  with st.spinner('Currently loading data...'):
    cluster_cont.plotly_chart(cluster_map(df_main), use_container_width=True)
    cluster_cont.markdown('---')
  with choro_cont:
    sel = st.selectbox('Selector for Choropleth Graph', shapeJoin.columns[5:28], help='Select the incident type you would like to see on the map. The darker the county, the more of selected incidents in that county. If you selected "drought", the county with the most droughts will appear darkest.')
    scale = getScale(sel)
    with st.spinner('Currently loading data...'):
      choro_cont.plotly_chart(ch_graph(sel, scale, df_main), use_container_width=True)

def render_page(df_main):
    graphs(df_main)

render_page(df_files[2])