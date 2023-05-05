# streamlit run 🏠_Home.py

import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import plotly_express as px
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title="NDD - Home",
                   page_icon="🏠", layout="wide")
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
def getData():
  d_df = pd.read_csv('data/us_disasters_m5.csv')
  g_df = pd.read_csv('data/updated_gun_violence_data.csv')

  return [d_df, g_df]
dfs = getData()
disaster_df = dfs[0]
gun_df = dfs[1]

askBot = st.button("🤖 Ask DisasterBot", use_container_width=False)
if askBot:
  switch_page('disasterbot')

# TEMPLATE GRAPH FOR SHOW --- BELOW THIS LINE
def example_graph():
    state = st.session_state.state_selector
    incident_frequency = disaster_df[disaster_df['state'] == state].groupby(by=["incident_type"]).count()[
        ['state']].sort_values(by='state')
    fig_incident_frequency = px.bar(
        incident_frequency,
        x=incident_frequency.index,
        y='state',
        labels={
            "incident_type": "Incident by Type",
            "state": "Count"
        },
        title="<b>Incident Frequency</b>",
        color=incident_frequency.index,
        text_auto=True
    )
    fig_incident_frequency.update_layout(
        xaxis=dict(tickmode="linear", autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    return fig_incident_frequency
# TEMPLATE GRAPH FOR SHOW --- ABOVE THIS LINE


with st.container():
    one_col, two_col = st.columns((1,2))
    one_col.image('images/logo-main.png', use_column_width=False, width=250)
    with two_col:
        st.markdown('# Welcome Home')
        st.write("##### Showing you the data you didn't know you need.")
        st.write("##### A little stuck? Head over to DisasterBot and ask it for some insights!")

st.markdown('---')

def state_change():
    st.markdown('---')
    st.selectbox(
        'What state would you like to hone in on?',
        ('TX', 'CA', 'WI'),
        key='state_selector')
    if st.session_state.state_selector:
        st.write('State you chose:', st.session_state.state_selector)
        st.markdown('---')
    else:
        print('000000000000000000000000000000 ERROR STATE NOT IN SESSION STATE 000000000000000000000000000000')

def date_change():
    st.write('Currently pulling from m5 dataset. Uses first value of incident begin date as starting date default and last value as ending date default. Assumes the incident_begin_date column is sorted chronologically.')
    # st.date_input("Start Date", value=pd.to_datetime("2021-01-31", format="%Y-%m-%d"), key='start_date')
    st.date_input("Start Date", value=pd.to_datetime(disaster_df.iloc[0]['incident_begin_date'], format="%Y-%m-%d"), key='start_date')
    st.date_input("End Date", value=pd.to_datetime(disaster_df.iloc[len(disaster_df)-1]['incident_begin_date'], format="%Y-%m-%d"), key='end_date')
    # st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"), key='end_date')
    if st.session_state.start_date and st.session_state.end_date:
        st.write('Start date you chose:', st.session_state.start_date.strftime('%Y-%m-%d'))
        st.write('End date you chose:', st.session_state.end_date.strftime('%Y-%m-%d'))
    else:
        print('000000000000000000000000000000 ERROR DATE NOT IN SESSION STATE 000000000000000000000000000000')

# QUICK GLANCE --- BELOW THIS LINE
def quick_glance():
    # st.write('Maybe have this with a choropleth of all merged data in database? Or potentially have insights from DisasterBot here, if possible? Thinking that if data is scraped live from the internet, could have this become a "Latest Incident" section.')

    # st.title('Quick Glance')
    total_incidents = int(disaster_df["incident_type"].count())
    total_states = (disaster_df['state'].nunique() + gun_df['state'].nunique())
    top_incident = disaster_df['incident_type'].value_counts().index[0]
    top_state = (disaster_df.groupby('state')['incident_type'].count()).idxmax()

    top_areas = (disaster_df.loc[disaster_df['designated_area'] != 'Statewide']).groupby(['designated_area', 'state']).count().sort_values(by='incident_type', ascending=False).head(3)
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

        total_crime = int(gun_df["incident_id"].count())
        top_crime = gun_df['congressional_district'].value_counts().index[0]
        top_crime_state = (gun_df.groupby('state')['incident_id'].count()).idxmax()

        top_crime_areas = gun_df.groupby(['city_or_county', 'state']).count().sort_values(by='incident_id', ascending=False).head(3)
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
      with st.container():
          image_col, text_col = st.columns((1,2))
          with image_col:
              st.image("https://cdn-images-1.medium.com/max/906/1*dVSDol9pouoO9IX_E_-35Q.png", caption='PLACEHOLDER')
          with text_col:
              st.subheader('Interactive Data')
              st.write('You can expect a fully interactive experience. All of our graphs have interactivity built in. Want to zoom in on a location? Just click and drag the box around the part you want to zoom in on!')
      with st.container():
          image_col, text_col = st.columns((1,2))
          with image_col:
              st.image("https://cdn-images-1.medium.com/max/906/1*dVSDol9pouoO9IX_E_-35Q.png", caption='PLACEHOLDER')
          with text_col:
              st.subheader('Hone in on Data')
              st.write('Do you want to only look at data from a specific state? Head over to our "Custom ⚙️" tab on the Dashboard page. There you can select specific states as well as specific incidents to hone in on.')
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

def render_page():
  quick_glance()
  st.markdown('---')
  dev_info()


render_page()