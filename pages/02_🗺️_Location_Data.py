import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
# for choropleth graph
import geopandas as gpd
import plotly.express as px
import json



# Sets browser tab information
st.set_page_config(page_title="NDD - Location Data",
                   page_icon="🗺️", layout="wide")

# Adds title to top of page
st.title("🗺️ Disaster Locations Dashboard")
st.markdown("This is an interactive scatter map of disasters in the United States.  &nbsp;Hovering over a marked location will show more details.")
st.markdown("##")

df_main = pd.read_csv('data/short_details_for_storm_events.csv')

def scatter_map(df):
    hover_template = '<b>%{customdata[0]}</b><br>' + \
                     'Injuries: %{customdata[1]}<br>' + \
                     'Cost: %{customdata[2]}<br>' + \
                     'Date: %{customdata[3]} %{customdata[4]}<extra></extra>'

    scatter_map = go.Figure(go.Scattergeo(
        lat=df['BEGIN_LAT'],
        lon=df['BEGIN_LON'],
        mode='markers',
        marker=dict(
            size=1.5,
            line=dict(width=1, color='red'),
        ),
        hovertemplate=hover_template,
        customdata=df[['EVENT_TYPE', 'INJURIES_DIRECT', 'DAMAGE_PROPERTY', 'MONTH_NAME', 'YEAR']].values
    ))

    scatter_map.update_layout(
        title='U.S. Disasters Latitude / Longitude Locations',
        geo=dict(
            scope='usa',
            showsubunits=True,
            subunitcolor='white',
            subunitwidth=2,
            center=dict(lat=39.8, lon=-98.5),
            projection=dict(type='albers usa'),
            projection_scale=0.9,
            showcountries=True,
            bgcolor="rgba(14,17,23,1)",
            countrycolor="white",
        ),
        margin=dict(l=0, r=0, t=35, b=0),
    )

    # Customizes the map to add lakes and rivers
    scatter_map.update_geos(
        resolution=50,
        showlakes=True,
        lakecolor='Blue',
        showrivers=True,
        rivercolor='Blue',
    )

    return scatter_map


# --- CHOROPLETH GRAPH ---
def ch_graph():
  # Load the shapefile using geopandas
  shapefile = gpd.read_file('data/cb_2018_us_county_20m.shp')
  crop_dec = pd.read_excel('data/crop-year-2014-disaster-declarations-1.xls')

  crop_dec = crop_dec.rename(columns = {
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

  shapefile['GEOID'] = shapefile['GEOID'].astype(str)
  crop_dec['fips'] = crop_dec['fips'].astype(str)
  crop_dec['fips'] = [x if len(x) == 5 else "0"+x for x in crop_dec['fips']]

  shapeJoin = crop_dec.merge(shapefile, right_on = 'GEOID', left_on = 'fips')

  # Set custom color scale based on range of drought values
  scale = [[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,0)']]

  # Convert the geometry column to a GeoSeries
  geometry = gpd.GeoSeries(shapeJoin['geometry'])

  # Convert the GeoSeries to JSON format
  geojson = json.loads(geometry.to_json())


  # --- Selector for Choropleth Graph ---
    # currently "hardcoded" for columns 5 through 28
  sel = st.selectbox('Selector for Choropleth Graph', shapeJoin.columns[5:28], help='Select the incident type you would like to see on the map. The darker the county, the more of selected incidents in that county. If you selected "drought", the county with the most droughts will appear darkest.')

  # Filter the shapeJoin dataframe based on the selected incident type
  shapeJoin_filtered = shapeJoin[shapeJoin[sel] == 1]
  print(shapeJoin_filtered.columns)
  # Use Plotly Express to create the choropleth graph
  fig_ch = px.choropleth_mapbox(shapeJoin_filtered,
                      title='Choropleth Graph - Work in Progress',
                      geojson=geojson,
                      locations=shapeJoin_filtered.index,
                      color=sel,
                      opacity=0.2,
                      hover_name='County',
                      hover_data={
                        sel: False,
                        'State': True,
                        'fips': True,
                        'Begin Date': True,
                        'End Date': True,
                      },
                      center=dict(lat=39.8, lon=-98.5),
                      zoom=3.0,
                      height=800,
                      mapbox_style="open-street-map",
                      color_continuous_scale=scale,
                      color_continuous_midpoint=0.5,
                      labels={sel: sel.capitalize()})

  return fig_ch

def graphs(df_main):
  # Creates a container on the page and displays the map
  scat_cont = st.container()
  choro_cont = st.container()

  scat_cont.plotly_chart(scatter_map(df_main), use_container_width=True)
  scat_cont.markdown('---')
  choro_cont.plotly_chart(ch_graph(), use_container_width=True)

def render_page(df_main):
  graphs(df_main)

render_page(df_main)
# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)