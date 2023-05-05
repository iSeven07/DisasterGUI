import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page
import time


st.set_page_config(page_title="NDD - Gun Violence Data",
                   page_icon="🚨", layout="wide")

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
# Sets browser tab information

# Adds title to top of page
st.title("🚨 Gun Violence Dashboard")
st.markdown("This is an interactive scatter map of Gun Violence in the United States.  &nbsp;Hovering over a marked location will show more details.")
st.markdown("##")


@st.cache_data
def get_data():
  crime_df = pd.read_csv('data/updated_gun_violence_data.csv')
  return crime_df


crime_df = get_data()


@st.cache_data
def animated_map(crime_df):
  animation_map = px.scatter_geo(crime_df,
                                 title='Gun Violence 2013 - 2018',
                                 lat='latitude',
                                 lon='longitude',
                                 #  size=(crime_df['n_killed'] + crime_df['n_injured']),
                                 projection='albers usa',
                                 center=dict(lat=37.2, lon=-89.3),
                                 color='state',
                                 hover_data=[
                                     'city_or_county',
                                     'date',
                                     'n_killed',
                                     'n_injured',
                                     'incident_characteristics',
                                 ],
                                 labels={
                                     'state': 'State',
                                     'longitude': 'Longitude',
                                     'latitude': 'Latitude',
                                     'city_or_county': 'City or County',
                                     'incident_characteristics': 'Incident Details',
                                     'n_killed': 'Killed',
                                     'n_injured': 'Injured',
                                     'date': 'Date'
                                 },
                                 animation_frame='month_year',
                                 )
  return animation_map


@st.cache_data
def scatter_map(crime_df):
  scatter_plot = px.scatter_geo(crime_df,
                                title='Gun Violence 2013 - 2018',
                                lat='latitude',
                                lon='longitude',
                                projection='albers usa',
                                center=dict(lat=37.2, lon=-89.3),
                                color='state',
                                hover_data=[
                                    'city_or_county',
                                    'n_killed',
                                    'n_injured',
                                    'incident_characteristics'
                                ],
                                labels={
                                    'state': 'State',
                                    'longitude': 'Longitude',
                                    'latitude': 'Latitude',
                                    'city_or_county': 'City or County',
                                    'incident_characteristics': 'Incident Details',
                                    'n_killed': 'Killed',
                                    'n_injured': 'Injured',
                                    'date': 'Date'
                                },
                                )
  return scatter_plot


def graphs(crime_df):
  askBot = st.button("🤖 Ask DisasterBot", use_container_width=False)
  if askBot:
    switch_page('disasterbot')
  # Creates a container on the page and displays the map
  animated_container = st.container()
  scatter_container = st.container()
  animated_container.plotly_chart(
    animated_map(crime_df), use_container_width=True)
  animated_container.markdown('---')
  scatter_container.plotly_chart(
    scatter_map(crime_df), use_container_width=True)


def render_page(crime_df):
  with st.spinner('Currently loading data...'):
    graphs(crime_df)


render_page(crime_df)
