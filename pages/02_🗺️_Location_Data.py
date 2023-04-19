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


def movie_map(df):

  the_years = [year for year in range(1950, 2024)]
  frames = []

  for i in range(24):
    frames.append(
      go.Frame(
        data=[
          go.Scattergeo(
            lon=df['BEGIN_LON'],
            lat=df['BEGIN_LAT'],
            mode="markers",
            marker=dict(
                    color='red',
                    size=(7 * i),
                  ),
          )
        ]
      )
    )

  scattergeo = go.Scattergeo(mode="markers")

  fig = go.Figure(data=[scattergeo], frames=frames)

  fig.update_layout(
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
        showland=True,
        landcolor="grey",
        countrycolor="white",

      ),
      updatemenus=[
          dict(
            type="buttons",
            showactive=True,
            buttons=[
              dict(
                label="Play",
                method="animate",
                args=[None,
                      dict(
                        frame=dict(duration=200, redraw=True),
                        fromcurrent=True,
                        mode="immediate",
                        ),
                ],
              ),
              dict(
                label="Pause",
                method="animate",
                args=[[None],
                      dict(
                        mode="immediate",
                        transition=dict(duration=0),
                        frame=dict(duration=0, redraw=True),
                      ),
                ],
              ),
            ],
          )
      ],
  )
  return fig


def slider_map(df):
# Website for the map animation: https://towardsdatascience.com/how-to-create-animated-scatter-maps-with-plotly-and-dash-f10bb82d357a
# Github for above link: https://github.com/ThibaudLamothe/dash-mapbox/blob/master/scripts/create_world_fig.py
# Mapbox link: https://www.mapbox.com/ (this is the plotly replacement)

    # Creates a dictionary of year and month for each event_id
  year_month = df_main['BEGIN_YEARMONTH'].tolist()
  event_id = df_main['EVENT_ID'].tolist()

# REFACTOR THIS TO USE 'YEAR' COLUMN INSTEAD OF 'BEGIN_YEARMONTH'
  dates = {}
  for i in range(len(year_month)):
    ym = year_month[i]
    id = event_id[i]
    if id not in dates:
      dates[id] = {}
    dates[id]['year'] = str(ym)[0:4]
    dates[id]['month'] = str(ym)[4:6]

  frames = [{
        # 'traces':[0],
        'name':'frame_{}'.format(date),
        'data':[{
            'type':'scattermapbox',
            'lat':df['BEGIN_LAT'],
            'lon':df['BEGIN_LON'],
            'marker':go.scattermapbox.Marker(
                size=5,
                color='red',
                showscale=True,
                colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
                # color_continuous_scale=px.colors.cyclical.IceFire,
            ),
            # 'customdata':np.stack((df.xs(day)['confirmed_display'], df.xs(day)['recovered_display'],  df.xs(day)['deaths_display'], pd.Series(df.xs(day).index)), axis=-1),
            # 'hovertemplate': "<extra></extra><em>%{customdata[3]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[2]}",
        }],
    } for date in year_month] # REFACTOR THIS TO USE 'YEAR' COLUMN INSTEAD OF 'BEGIN_YEARMONTH'

  data = frames[-1]['data']

  active_frame = len(dates.keys()) - 1

  # Defining the slider to navigate between frames
  sliders = [{
        'active':active_frame,
        'transition':{'duration': 0},
        'x':0.08,     #slider starting position
        'len':0.88,
        'currentvalue':{
            'font':{'size':15},
            'prefix':'📅 ', # Day:
            'visible':True,
            'xanchor':'center'
            },
        'steps':[{
            'method':'animate',
            'args':[
                ['frame_{}'.format(str(date)[0:4])],
                {
                    'mode':'immediate',
                    'frame':{'duration':250, 'redraw': True}, #100
                    'transition':{'duration':100} #50
                }
                ],
            'label':str(date)[0:4]
        } for date in year_month] # REFACTOR THIS TO USE 'YEAR' COLUMN INSTEAD OF 'BEGIN_YEARMONTH'
    }]

  play_button = [{
        'type':'buttons',
        'showactive':True,
        'y':-0.08,
        'x':0.045,
        'buttons':[{
            'label':'🎬', # Play
            'method':'animate',
            'args':[
                None,
                {
                    'frame':{'duration':250, 'redraw':True}, #100
                    'transition':{'duration':100}, #50
                    'fromcurrent':True,
                    'mode':'immediate',
                }
            ]
        }]
    }]

  layout = go.Layout(
        height=600,
        autosize=True,
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        mapbox={
            'accesstoken': '', # Mapbox access token goes here
            'bearing':0,
            'center':{'lat':39.8, 'lon':-96.3},
            'pitch':0,
            'zoom':2.9,
            'style':'dark',
        },
        updatemenus=play_button,
        sliders=sliders,
        margin={"r":100,"t":0,"l":0,"b":100}
    )

  return go.Figure(data=data, layout=layout, frames=frames)

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
                          ,'Hail': 'hail'
                          ,'Wind, High Winds': 'high wind'
                          ,'Fire, Wildfire': 'fire'
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

  #shapeJoin['geometry'] = shapeJoin['geometry'].apply(lambda x: x.__geo_interface__)

  # Set custom color scale based on range of drought values
  scale = [[0, 'rgb(255,255,255)'], [1, 'rgb(0,255,0)']]
  #color_mapper = lambda x: 0 if x == 0 else 1

  # Convert the geometry column to a GeoSeries
  geometry = gpd.GeoSeries(shapeJoin['geometry'])

  # Convert the GeoSeries to JSON format
  geojson = json.loads(geometry.to_json())


  # Use Plotly Express to create the choropleth graph
  fig_ch = px.choropleth_mapbox(shapeJoin, 
                      #geojson=shapefile.geometry.__geo_interface__, 
                      title='Choropleth Graph - Work in Progress',
                      geojson=geojson, 
                      locations=shapeJoin.index, 
                      color='drought', 
                      hover_name='County',
                      center=dict(lat=39.8, lon=-98.5),
                      zoom=3.0,
                      height=800,
                      #scope='usa',
                      mapbox_style="open-street-map",
                      color_continuous_scale=scale,
                      #color_discrete_map={0: 'rgb(255,255,255)', 1: 'rgb(0,255,0)'},
                      color_continuous_midpoint=0.5,
                      labels={'drought': 'Drought'})

  return fig_ch

def graphs(df_main):
  # Creates a container on the page and displays the map
  map_container = st.container()
  map_container.plotly_chart(scatter_map(df_main), use_container_width=True)
  map_container.markdown('---')
  map_container.plotly_chart(ch_graph(), use_container_width=True)

  # IMPORTANT: READ BELOW
  # BEFORE YOU UNCOMMENT THE CODE BELOW YOU NEED TO CHANGE THE DATAFRAME TO ONLY TAKE IN 100 ROWS
  # CHANGE IT ON LINE 16 FROM: df_main = pd.read_csv('data/short_details_for_storm_events.csv')
  # TO: df_main = pd.read_csv('data/short_details_for_storm_events.csv', nrows=100)
  # IMPORTANT: READ ABOVE
  # st.markdown('# ---Below Maps Under Development---')
  # map_container = st.container()
  # map_container.plotly_chart(movie_map(df_main), use_container_width=True)
  # st.markdown('---')
  # map_container = st.container()
  # map_container.plotly_chart(slider_map(df_main), use_container_width=True)

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