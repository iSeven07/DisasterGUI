import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="NDD - Location Data",
                   page_icon="🗺️", layout="wide")

st.title("🗺️ Disaster Locations Dashboard")

df = pd.read_csv('locations_for_storm_events.csv', nrows=10000)

scatter_map = go.Figure(go.Scattergeo(lat=df['LATITUDE'], lon=df['LONGITUDE']))
scatter_map.update_layout(
    title='Disasters Latitude / Longitude Location',
    geo=dict(
        scope='usa',
        showsubunits=True,
        center=dict(lat=37.0902, lon=-95.7129),
        projection=dict(type='albers usa'), #equirectangular
        showcountries=False,
    )
)

map_container = st.container()
map_container.plotly_chart(scatter_map, use_container_width=True)

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)