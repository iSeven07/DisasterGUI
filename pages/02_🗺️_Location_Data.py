import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Sets browser tab information
st.set_page_config(page_title="NDD - Location Data",
                   page_icon="🗺️", layout="wide")

# Adds title to top of page
st.title("🗺️ Disaster Locations Dashboard")
st.markdown("##")

# Reads in the csv file and limits the number of rows it reads to 10000
df = pd.read_csv('locations_for_storm_events.csv', nrows=10000)

def scatter_map(df):
  # Creation of the scatter plot map [SCATTER PLOT MAP]
  scatter_map = go.Figure(go.Scattergeo(lat=df['LATITUDE'], lon=df['LONGITUDE'], mode='markers', marker=dict(size=1.5, line=dict(width=1, color='red'))))

  # Refines the scope of the scatter plot map [SCATTER PLOT MAP]
  scatter_map.update_layout(
      title='U.S. Disasters Latitude / Longitude Locations',
      geo=dict(
          scope='usa',
          showsubunits=True,
          subunitcolor='white',
          subunitwidth=2,
          center=dict(lat=37.0902, lon=-95.7129),
          projection=dict(type='albers usa'),
          projection_scale=0.9,
          showcountries=False,
          bgcolor="rgba(14,17,23,1)",
      ),
      margin=dict(l=0, r=0, t=35, b=0),
  )

  # Customizes the map to add lakes and rivers [SCATTER PLOT MAP]
  scatter_map.update_geos(
      resolution=50,
      showlakes=True,
      lakecolor='Blue',
      showrivers=True,
      rivercolor='Blue',
  )

  # Creates a container on the page and displays the map [SCATTER PLOT MAP]
  map_container = st.container()
  map_container.plotly_chart(scatter_map, use_container_width=True)

def load_graphs():
  scatter_map(df)

load_graphs()

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)