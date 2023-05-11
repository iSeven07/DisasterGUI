# streamlit run 🏠_Home.py

import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import json
import numpy as np
import plotly_express as px
from streamlit_extras.switch_page_button import switch_page
#choropleth
import plotly.graph_objs as go
#from dotenv import load_dotenv # can just use import os for the env token
import os
import geopandas as gpd
from urllib.request import urlopen



st.set_page_config(page_title="NDD - Home",
                   page_icon="🏠", layout="wide")
add_logo("images/lrw-color.png")
#load_dotenv()
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
@st.cache_data
def getData():
  d_df = pd.read_csv('data/us_disaster_declarations.csv')
  g_df = pd.read_csv('big_data/crime.csv')
  with open('data/state_info.json', 'r') as f:
    s_info = json.load(f)
  s_file = gpd.read_file('data/cb_2018_us_county_20m.shp')

  return [d_df, g_df, s_info, s_file]

def reverse_dictionary(dictionary):
    reversed_dict = {}
    for key, value in dictionary.items():
        reversed_dict[value] = key
    return reversed_dict

dfs = getData()
disaster_df = dfs[0]
gun_df = dfs[1]
state_info = dfs[2]
shape_file = dfs[3]
try:
  token = os.environ["MAPBOX_API"]
  px.set_mapbox_access_token(token)
except KeyError:
  st.write("API KEY was not found!")

def header():
  with st.container():
    one_col, two_col = st.columns((1,2))
    one_col.image('images/logo-main.png', use_column_width=False, width=250)
    with two_col:
        st.markdown('# Welcome Home')
        st.write("##### Showing you the data you didn't know you need.")
        st.write("##### A little stuck? Head over to DisasterBot and ask it for some insights!")
  askBot = st.button("🤖 Ask DisasterBot", use_container_width=False)
  if askBot:
    switch_page('disasterbot')

def example_choro():
  filtered_disaster_df = disaster_df[disaster_df['state'].isin(getSelection())]
  with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
  fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_disaster_df.fips, z=filtered_disaster_df.ia_program_declared,
                                    colorscale="Viridis", zmin=0, zmax=1,
                                    marker_opacity=0.5, marker_line_width=0))
  # fig.add_scattermapbox(lat = gun_df['latitude'],
  #                       lon = gun_df['longitude'],
  #                       mode = 'markers+text',
  #                       text = 'example',  #a list of strings, one  for each geographical position  (lon, lat)
  #                       below='',
  #                       marker_size=3,
  #                       marker_color='rgb(235, 0, 100)')

  fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=2.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
  fig.update_layout(title='Choropleth Layering', margin={"r":0,"t":35,"l":0,"b":0})

  return fig

def cluster_map():
  filtered_gun_df = gun_df[gun_df['state'].isin([state_info.get(abbreviation) for abbreviation in getSelection()])]
  filtered_gun_df['total_killed'] = filtered_gun_df.groupby('city_or_county')['n_killed'].transform('sum')
  filtered_gun_df['total_injured'] = filtered_gun_df.groupby('city_or_county')['n_injured'].transform('sum')
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

def date_change():
    st.write('Currently pulling from m5 dataset. Uses first value of incident begin date as starting date default and last value as ending date default. Assumes the incident_begin_date column is sorted chronologically.')
    st.date_input("Start Date", value=pd.to_datetime(disaster_df.iloc[0]['incident_begin_date'], format="%Y-%m-%d"), key='start_date')
    st.date_input("End Date", value=pd.to_datetime(disaster_df.iloc[len(disaster_df)-1]['incident_begin_date'], format="%Y-%m-%d"), key='end_date')
    if st.session_state.start_date and st.session_state.end_date:
        st.write('Start date you chose:', st.session_state.start_date.strftime('%Y-%m-%d'))
        st.write('End date you chose:', st.session_state.end_date.strftime('%Y-%m-%d'))
    else:
        print('000000000000000000000000000000 ERROR DATE NOT IN SESSION STATE 000000000000000000000000000000')

def filter_data():
  st.subheader('Looking to hone in?')
  # st.selectbox('What state would you like to hone in on?', state_info.values(), key='state_selected')
  st.selectbox('What dataset would you like?', ['Ozark Region Plus', 'All Data'], key='state_selected')

def getSelection():
  if st.session_state.state_selected == 'Ozark Region Plus':
    return ['MO', 'TN', 'AR', 'KY', 'KS']
  else:
    return list(state_info.keys())

# QUICK GLANCE --- BELOW THIS LINE
def quick_glance():
    # Filter the DataFrames based on the included states
    filtered_disaster_df = disaster_df[disaster_df['state'].isin(getSelection())]
    filtered_gun_df = gun_df[gun_df['state'].isin([state_info.get(abbreviation) for abbreviation in getSelection()])]
    # filtered_gun_df['state'] = filtered_gun_df['state'].replace(reverse_dictionary(state_info))
    # filtered_gun_df['state'] = filtered_gun_df['state'].map(reverse_dictionary(state_info))
    # print(filtered_gun_df['state'])
    # st.title('Quick Glance')
    total_incidents = int(filtered_disaster_df["incident_type"].count())
    #total_states = (filtered_disaster_df['state'].nunique() + gun_df['state'].nunique())
    # print(len(set(filtered_disaster_df['state']).union(set(filtered_gun_df['state']))))
    # print(filtered_disaster_df['state'])
    # print(set(filtered_disaster_df['state']).union(set(filtered_gun_df['state'])))
    # for state in total_states:
    #   if state.len() == 2:
   # gun_df['state'] = gun_df['state'].replace(reverse_dictionary(state_info))
    total_states = len(set(filtered_disaster_df['state']).union(set(filtered_gun_df['state'].replace(reverse_dictionary(state_info)))))
    # total_states = len(set(filtered_disaster_df['state']))
    top_incident = filtered_disaster_df['incident_type'].value_counts().index[0]
    top_state = (filtered_disaster_df.groupby('state')['incident_type'].count()).idxmax()

    top_areas = (filtered_disaster_df.loc[filtered_disaster_df['designated_area'] != 'Statewide']).groupby(['designated_area', 'state']).count().sort_values(by='incident_type', ascending=False).head(3)
    top_areas = (top_areas[['incident_type']].rename(columns={'incident_type': 'count'})).reset_index()

    with st.container():
      # Natural Disaster Quick Glance
        st.subheader('Natural Disasters Info')
        col_one, col_two, col_three = st.columns(3)
        with col_one:
            st.markdown('#####')
            st.subheader(f"Natural Incidents: :red[{total_incidents}]")
            st.subheader(f"Most Natural Incident: :red[{top_incident}]")

        with col_two:
            st.markdown('#####')
            st.subheader(f"Total States: :blue[{total_states}]")
            st.subheader(f"Most Natural Disasters: :blue[{top_state}]")

        with col_three:
            stringText = ''
            for index, row in top_areas.iterrows():
                stringText += (f"{index+1}. {row['designated_area']}, {row['state']}: {row['count']} incidents<br>")
            st.markdown('<p style="font-weight: 600; font-color: white; font-size: 30px; margin: auto;">Top 3 Areas for Natural Disasters</p>' + stringText, unsafe_allow_html=True)


        total_crime = int(filtered_gun_df["incident_id"].count())
        top_crime = filtered_gun_df['congressional_district'].value_counts().index[0]
        top_crime_state = (filtered_gun_df.groupby('state')['incident_id'].count()).idxmax()

        top_crime_areas = filtered_gun_df.groupby(['city_or_county', 'state']).count().sort_values(by='incident_id', ascending=False).head(3)
        top_crime_areas = (top_crime_areas[['incident_id']].rename(columns={'incident_id': 'count'})).reset_index()
        st.markdown('---')
      # Crime Quick Glance
        st.subheader('Crime Info')
        col_one, col_two, col_three = st.columns(3)
        with col_one:
            st.markdown('#####')
            st.subheader(f"Crime Incidents: :red[{total_crime}]")
            st.subheader(f"Congressional District with Most Crime: :red[{int(top_crime)}]")

        with col_two:
            st.markdown('#####')
            st.subheader(f"Total States: :blue[{total_states}]")
            st.subheader(f"Most Crime: :blue[{top_crime_state}]")

        with col_three:
            stringText = ''
            for index, row in top_crime_areas.iterrows():
                stringText += (f"{index+1}. {row['city_or_county']}, {row['state']}: {row['count']} incidents<br>")
            st.markdown('<p style="font-weight: 600; font-color: white; font-size: 30px; margin: auto;">Top 3 Areas for Crime</p>' + stringText, unsafe_allow_html=True)
# QUICK GLANCE --- ABOVE THIS LINE

def dev_info():
  # WHAT CAN YOU EXPECT --- BELOW THIS LINE
  with st.expander('What can you expect?'):
    st.markdown('#')
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("images/pic1.png", caption='Dashboard')
        with text_col:
            st.subheader('Interactive Dashboard')
            st.write('The Dashboard offers a quick glance of natural disasters that have been recorded across the country.  Visualizations of the data are customizable, so you can narrow the scope of data to single or multiple states.')
            st.markdown('#')
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("images/pic2.png", caption='Location Data')
        with text_col:
            st.subheader('Visualize the Data')
            st.write('The Location Data page has an interactive chloropleth map of the U.S. that allows you to see where extreme weather events have occurred over time.')
            st.markdown('#')
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("images/pic3.png", caption='Location Data')
        with text_col:
            st.subheader('Examine Crime Data')
            st.write('The Crime Data page has an animated graph of gun violence that has occurred over time.  Get more details for each event by hovering your cursor over the marked location.')
            st.markdown('#')
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("images/pic4.png", caption='Location Data')
        with text_col:
            st.subheader('Leverage the Power of AI')
            st.write('Ask DisasterBot a question in plain language and get fast answers!')
  # WHAT CAN YOU EXPECT --- ABOVE THIS LINE

  # ABOUT THIS APPLICATION --- BELOW THIS LINE
  with st.expander('About this application (Click to expand)'):
      st.write('Have this for dev notes / feature updates?')
      with st.container():
          image_col, text_col = st.columns((1,2))
          with image_col:
              st.image("https://cdn-images-1.medium.com/max/906/1*dVSDol9pouoO9IX_E_-35Q.png", caption='PLACEHOLDER')

          with text_col:
              st.subheader("A Multi-page Interactive Dashboard with Streamlit and Plotly")
              st.write("""
                  Our team chose to use Streamlit alongside Plotly and a few other tools to create this interactive data analysis dashboard. These tools allow us to create the lovely pages and graphs you are looking at right now.
                  """)
              st.markdown("[Filler Link](https://google.com)")

      with st.container():
          image_col, text_col = st.columns((1,2))
          with image_col:
              st.image("https://cdn-images-1.medium.com/max/906/1*hjhCIWGgLzOznTFwDyeIeA.png", caption='PLACEHOLDER')

          with text_col:
              st.subheader("This dashboard will see integration with AI")
              st.write("""
                  One thing our team prides itself on is our creativeness. We will be working hard throughout the next weeks to integrate AI into this data analysis tool. Keep a lookout for future updates!
                  """)
              st.markdown("[Filler Link](https://google.com)")
          st.write("Suggestions? Feel free to reach out to us!")
  # ABOUT THIS APPLICATION --- ABOVE THIS LINE

def graphs():
  choro_cont = st.container()
  # cluster_cont = st.container()
  # choro_cont.plotly_chart(choro_layered(), use_container_width=True)
  with st.spinner('Currently loading data...'):
    choro_cont.plotly_chart(example_choro(), use_container_width=True)
  # with st.spinner('Currently loading data...'):
  #   cluster_cont.plotly_chart(cluster_map(), use_container_width=True)

def render_page():
  header()
  st.markdown('---')
  filter_data()
  st.markdown('---')
  with st.spinner('Currently loading data...'):
    quick_glance()
  st.markdown('---')
  graphs()
  st.markdown('---')
  dev_info()


render_page()