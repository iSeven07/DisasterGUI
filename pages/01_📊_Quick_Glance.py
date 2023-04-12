import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly
import streamlit as st  # pip install streamlit
import datetime
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page

# Streamlit Documentation: https://docs.streamlit.io/
# Plotly: https://plotly.com/python/
# Pandas: https://www.w3schools.com/python/pandas/default.asp

st.set_page_config(page_title="NDD - Quick Glance",
                   page_icon="📊", layout="wide")

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-size: 24px; }
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)

@st.cache_data
def get_data():
  # ---- READ CSV ----
  df = pd.read_csv('us_disasters_m5.csv')
  # Should return the year, ie 2017
  df["year"] = pd.to_datetime(
    df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.year
  # Should return the date, ie 2011-02-27
  df["date"] = pd.to_datetime(
    df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.date
  return df


df = get_data()

# ---- DEFAULT QUERY ----
defaultStates = list(df["state"].unique())
defaultQuery = df.query(f'state == {defaultStates}')

# ---- FILTER BOOLEAN ----
show_filters = False

# ---- SIDEBAR ----

# Potentially future idea to refactor sidebar in a better manner
# class mySidebar:
#    i = 1234

#    def getI(self):
#       return self.i

def sidebar(df):
    # Future use for AI Button
    askBot = st.sidebar.button("Ask DisasterBot", use_container_width=True)
    if askBot:
        switch_page('disasterbot')

def filters(df):
    fcol1, fcol2 = st.columns(2)

    with fcol1:
      # Below variable IS USED, just used in string below on line 63
      state = st.multiselect(
          "State Selections",
          options=df["state"].unique(),
          default=df["state"].unique()

      )
    with fcol2:
      # Below variable IS USED, just used in string below on line 63
      incident_type = st.multiselect(
          "Incident Selections",
          options=df["incident_type"].unique(),
          default=df["incident_type"].unique(),
          key="incident_select"
      )
    # st.sidebar.header("Features In Progress")
    # st.sidebar.date_input("Select Start Date", datetime.date(2011, 1, 1))
    # st.sidebar.date_input("Select End Date")
    # Provides results to graphs for active filters
    global DF_SELECTION
    DF_SELECTION = df.query(
        "state == @state & incident_type == @incident_type"
    )
# ---- MAINPAGE ----

def top_info():
  st.title("📊 Natural Disaster Dashboard")
  st.markdown("##")

  # Top portion for totals
  st.title('Quick Glance')
  total_incidents = int(df["incident_type"].count())
  total_states = df['state'].nunique()
  top_incident = df['incident_type'].value_counts().index[0]
  top_state = (df.groupby('state')['incident_type'].count()).idxmax()
  #top_incident = incident_counts.index[0]

  left_column, right_column, blank_column2 = st.columns(3)

  with left_column:
    st.subheader(f"Total Incidents: :red[{total_incidents}]")
    st.subheader(f"Top Incident: :red[{top_incident}]")
  with right_column:
    st.subheader(f"Total States: :blue[{total_states}]")
    st.subheader(f"Most Disasters: :blue[{top_state}]")
  with blank_column2:
    st.empty()
  st.markdown("---")

# ---- GRAPHS ----
# Total Incidents in each State [BAR CHART]
def incident_by_state(filter=defaultQuery):
  incidents_by_state = (
      filter.groupby(by=["state"]).count()[["incident_type"]].sort_values(by="incident_type") #Look into validating sort_values usage
  )

  fig_incidents_by_state = px.bar(incidents_by_state, y=incidents_by_state.index,
                                  x="incident_type", labels={"incident_type": "No. Incidents", "state": "State"}, color=incidents_by_state.index, title="Total Incidents in each State")

  fig_incidents_by_state.update_layout(
      yaxis=dict(autorange="reversed")
      )  # Sorts Bar Chart
  return fig_incidents_by_state

# Incident Frequency [BAR CHART]
def incident_freq(filter=defaultQuery):
    incident_frequency = filter.groupby(by=["incident_type"]).count()[
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

# Number of incidents per year [LINE GRAPH]
def incidents_per_year(filter=defaultQuery):
    events_per_date = filter.groupby(
    'year').size().reset_index(name='events_count')

    fig_year = px.line(events_per_date, x="year",
                    y='events_count', title="Incidents by Year")

    return fig_year

# Incident types by year [SCATTER GRAPH]
def incident_type_year(DF_SELECTION=defaultQuery):
    fig_scatter = go.Figure(data=go.Scattergl(
        x=DF_SELECTION['incident_begin_date'],
        y=DF_SELECTION['incident_type'],
        text='State: ' + DF_SELECTION['state'] +
        '<br>Area: ' + DF_SELECTION['designated_area'] +
        '<br>Title: ' + DF_SELECTION['declaration_title'] +
        '<br>Type: ' + DF_SELECTION['incident_type'] +
        '<br>Begun: ' + DF_SELECTION['incident_begin_date'] +
        '<br>Ended: ' + DF_SELECTION['incident_end_date'],
        mode='markers',
        hovertemplate='%{text}'
    ))
    fig_scatter.update_layout(title='Incident Type by Year',
                            xaxis_title='Year', yaxis_title='Event')
    return fig_scatter

# ---- RENDER ----
def graphs(filter=defaultQuery):
    left_column, right_column = st.columns(2, gap='medium')
    left_column.plotly_chart(incident_freq(filter), use_container_width=True)
    right_column.plotly_chart(incident_by_state(filter), use_container_width=True)

    st.markdown("---")
    bottom_row = st.container()
    bottom_row.plotly_chart(incidents_per_year(filter), use_container_width=True)

    st.markdown("---")
    scatter_row = st.container()
    scatter_row.plotly_chart(incident_type_year(filter), use_container_width=True)

# ---- RENDER CUSTOM GRAPH PAGES ----
def graphs_f(filter):
    left_column, right_column = st.columns(2, gap='medium')
    left_column.plotly_chart(incident_freq(filter), use_container_width=True)

def render_page(df):
  sidebar(df)
  top_info()
  st.title('Visualizations')
  tab1, tab2, tab3, tab4 = st.tabs(["All 📈", "Fire 🔥", "Storms 🌩️", "Custom ⚙️"])
  with tab1:
    graphs()
  with tab2:
    df_fire = df.query('incident_type == ["Fire"]')
    graphs(df_fire)
  with tab3:
    df_storms = df.query('incident_type == ["Severe Storm(s)"]')
    graphs(df_storms)
  with tab4:
    filters(df)
    graphs(DF_SELECTION)
    

render_page(df)


