import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page
import time
import json
from urllib.request import urlopen


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
try:
  st.subheader('Your current data view: ' + st.session_state.state_selected)
except:
  st.subheader('Your current data view: Ozark Region Plus')
st.markdown("This is an interactive scatter map of Gun Violence in the United States.  &nbsp;Hovering over a marked location will show more details.")
st.markdown("##")


@st.cache_data
def get_data():
  # crime_df = pd.read_csv('data/updated_gun_violence_data.csv')
  crime_df = pd.read_csv('data/crime.csv')
  with open('data/state_info.json', 'r') as f:
    s_info = json.load(f)
  return [crime_df, s_info]


data_sets = get_data()
crime_df = data_sets[0]
state_info = data_sets[1]

def getSelection():
  try:
    if st.session_state.state_selected == 'Ozark Region Plus':
      return ['MO', 'TN', 'AR', 'KY', 'KS']
    else:
      return list(state_info.keys())
  except:
    return  ['MO', 'TN', 'AR', 'KY', 'KS']


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

def cluster_map(crime_df):
  filtered_gun_df = crime_df[crime_df['state'].isin([state_info.get(abbreviation) for abbreviation in getSelection()])]
  filtered_gun_df['total_incidents'] = filtered_gun_df.groupby('city_or_county')['incident_id'].transform('count')
  # https://plotly.com/python/scattermapbox/
  fig = px.scatter_mapbox(filtered_gun_df, lat='latitude', lon='longitude', size='total_incidents', color='total_incidents', color_continuous_scale=px.colors.sequential.OrRd)
  fig.update_layout(title_text ='Crime Data', mapbox = dict(center=dict(lat=39.8, lon=-98.5),  #change to the center of your map
                                  zoom=3, #change this value correspondingly, for your map
                                  style="dark",  # set your prefered mapbox style
                               ))
  # fig.update_traces(cluster=dict(enabled=True))
  fig.update_traces(
    hovertemplate='<b>City/County:</b> %{customdata[0]}<br>'
                  '<b>Total Incidents:</b> %{customdata[1]}<br>',
    customdata=filtered_gun_df[['city_or_county', 'total_incidents']]
)

  return fig


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
  # scatter_container.plotly_chart(
  #   scatter_map(crime_df), use_container_width=True)
  scatter_container.plotly_chart(
    cluster_map(crime_df), use_container_width=True)


def render_page(crime_df):
  with st.spinner('Currently loading data...'):
    graphs(crime_df)


render_page(crime_df)
