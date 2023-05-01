# streamlit run 🏠_Home.py

import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import plotly_express as px

st.set_page_config(page_title="NDD - Home",
                   page_icon="🏠", layout="wide")
add_logo("images/lrw-color.png")

# TEMPORARY FOR QUICK GLANCE --- BELOW THIS LINE
df = pd.read_csv('data/us_disasters_m5.csv')
# TEMPORARY FOR QUICK GLANCE --- ABOVE THIS LINE
# TEMPLATE GRAPH FOR SHOW --- BELOW THIS LINE
def example_graph(df):
    state = st.session_state.state_selector
    incident_frequency = df[df['state'] == state].groupby(by=["incident_type"]).count()[
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
    one_col.image('images/logo-main.png', use_column_width=True)
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
    st.date_input("Start Date", value=pd.to_datetime(df.iloc[0]['incident_begin_date'], format="%Y-%m-%d"), key='start_date')
    st.date_input("End Date", value=pd.to_datetime(df.iloc[len(df)-1]['incident_begin_date'], format="%Y-%m-%d"), key='end_date')
    # st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"), key='end_date')
    if st.session_state.start_date and st.session_state.end_date:
        st.write('Start date you chose:', st.session_state.start_date.strftime('%Y-%m-%d'))
        st.write('End date you chose:', st.session_state.end_date.strftime('%Y-%m-%d'))
    else:
        print('000000000000000000000000000000 ERROR DATE NOT IN SESSION STATE 000000000000000000000000000000')





# TEMPORARY FOR QUICK GLANCE --- BELOW THIS LINE
def example_glance():
    st.write('Maybe have this with a choropleth of all merged data in database? Or potentially have insights from DisasterBot here, if possible? Thinking that if data is scraped live from the internet, could have this become a "Latest Incident" section.')

    st.title('Quick Glance')
    total_incidents = int(df["incident_type"].count())
    total_states = df['state'].nunique()
    top_incident = df['incident_type'].value_counts().index[0]
    top_state = (df.groupby('state')['incident_type'].count()).idxmax()

    top_areas = (df.loc[df['designated_area'] != 'Statewide']).groupby(['designated_area', 'state']).count().sort_values(by='incident_type', ascending=False).head(3)
    top_areas = (top_areas[['incident_type']].rename(columns={'incident_type': 'count'})).reset_index()

    with st.container():
        left_column, right_column, blank_column2 = st.columns(3)
        with left_column:
            st.markdown('#####')
            st.subheader(f"Total Incidents: :red[{total_incidents}]")
            st.subheader(f"Top Incident: :red[{top_incident}]")

        with right_column:
            st.markdown('#####')
            st.subheader(f"Total States: :blue[{total_states}]")
            st.subheader(f"Most Disasters: :blue[{top_state}]")

        with blank_column2:
            stringText = ''
            for index, row in top_areas.iterrows():
                stringText += (f"{index+1}. {row['designated_area']}, {row['state']}: {row['count']} incidents<br>")
            st.markdown('<p style="font-weight: 600; font-color: white; font-size: 30px; margin: auto;">Top 3 Areas</p>' + stringText, unsafe_allow_html=True)
    with st.expander('Not sure if expander for graph, or have it displayed by default'):
        state_change()
        ex_graph_cont = st.container()
        ex_graph_cont.plotly_chart(example_graph(df), use_container_width=True)
    with st.expander('Temporary Date Session Example'):
        date_change()
# TEMPORARY FOR QUICK GLANCE --- ABOVE THIS LINE


example_glance() # TEMPORARY FOR QUICK GLANCE



st.markdown('---')
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

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)