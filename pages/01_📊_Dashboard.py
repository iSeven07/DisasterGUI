import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly
import streamlit as st  # pip install streamlit
import datetime
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo


# Streamlit Documentation: https://docs.streamlit.io/
# Plotly: https://plotly.com/python/
# Pandas: https://www.w3schools.com/python/pandas/default.asp

st.set_page_config(page_title="NDD - Dashboard",
                   page_icon="📊", layout="wide")

add_logo("images/lrw-color.png")

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-size: 24px; }
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
def get_data():
  # ---- READ CSV ----
  df = pd.read_csv('data/us_disaster_declarations.csv')
  # Should return the year, ie 2017
  df["year"] = pd.to_datetime(
    df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.year
  # Should return the date, ie 2011-02-27
  df["date"] = pd.to_datetime(
    df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.date
  return df


df_main = get_data()

# ---- DEFAULT QUERY ----
#defaultStates = list(df_main["state"].unique())
defaultStates = list(df_main["state"].unique())


def getSelection():
  try:
   if st.session_state.state_selected == 'Ozark Region Plus':
      return ['MO', 'TN', 'AR', 'KY', 'KS']
   else:
      return defaultStates
  except:
      return ['MO', 'TN', 'AR', 'KY', 'KS']

defaultQuery = df_main.query(f'state == {getSelection()}')


# generate a unique color for each state
color_dict = {}
for i, state in enumerate(df_main['state'].unique()):
  # calculate the color based on a formula using the state index
  color = 'rgb(' + ','.join(map(str, [((i + 5) * 71) % 255, ((i + 5) * 83) % 255, ((i + 5) * 97) % 255])) + ')'
  color_dict[state] = color


def filters(df):
    fcol1, fcol2 = st.columns(2)

    with fcol1:
      # Below variable IS USED, just used in string below on line 63
      state = st.multiselect(
          "State Selections",
          # options=df["state"].unique(),
          # default=df["state"].unique()
          options=getSelection(),
          default=getSelection()

      )
      try:
        state_selected=st.session_state.state_selected
      except:
         state_selected='Ozark Region Plus'

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
    try:
      # Not sure that this is needed, but leaving for now for future use
      if st.session_state.state_selected:
        DF_SELECTION = df.query(
      #    "state == @state & incident_type == @incident_type"
          "state == @state & incident_type == @incident_type",
        )
      else:
        DF_SELECTION = df.query(
          "state == @state & incident_type == @incident_type",
        )
    except:
      DF_SELECTION = df.query(
        "state == @state & incident_type == @incident_type",
      )

# ---- MAINPAGE ----

def top_info(df):
  st.title("📊 Disaster Dashboard")
  # EXAMPLE SESSION STATE
  try:
    st.subheader('Your current data view: ' + st.session_state.state_selected)
  except:
    st.subheader('Your current data view: Ozark Region Plus')

  st.markdown("##")

  askBot = st.button("🤖 Ask DisasterBot", use_container_width=False)
  if askBot:
    switch_page('disasterbot')


# ---- GRAPHS ----
# Total Incidents in each State [BAR CHART]

def incident_by_state(filter):
  incidents_by_state = (filter.groupby(by=["state"]).count()[["incident_type"]].sort_values(by="incident_type"))

  fig_incidents_by_state = px.bar(
    incidents_by_state,
    y=incidents_by_state.index,
    x="incident_type",
    labels={"incident_type": "No. Incidents", "state": "State"},
    color=incidents_by_state.index,
    # color=incidents_by_state.index.map(color_dict),
    # color_discrete_map=color_dict,
    title="Total Incidents in each State")

  fig_incidents_by_state.update_layout(
      yaxis=dict(autorange="reversed")
  )  # Sorts Bar Chart
  return fig_incidents_by_state

# Incident Frequency [BAR CHART]
def incident_freq(filter):
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
def incidents_per_year(filter):
 # filter['year_month'] = pd.to_datetime(filter['incident_begin_date']).dt.strftime("%Y-%m")
  # Fixes Pandas "A value is trying to be set on a copy of a slice from a DataFrame" warning
  filter_copy = filter.copy()
  filter_copy.loc[:, 'year_month'] = pd.to_datetime(filter_copy['incident_begin_date']).dt.strftime("%Y-%m")
  df_grouped = filter_copy.groupby(['incident_type', 'year_month']).size().reset_index(name='count')
  fig_year = px.line(df_grouped, x='year_month', y='count', color='incident_type', markers=True)

  fig_year.update_layout(
        title='Incidents Over Time',
        xaxis_title='Year', yaxis_title='Count',
        legend=dict(title='Color of Incident')
        )

  return fig_year


# Incident types by year [SCATTER GRAPH]
def incident_type_year(filter):
    df = filter

    traces = []
    state_color_dict = {}
    for incident_type in df['incident_type'].unique():
        # select data only for the current incident type
        df_selection = df[df['incident_type'] == incident_type]
        for state in df_selection['state'].unique():
            if state not in state_color_dict:
                # assign a color to the state if it has not been assigned one yet
                state_color_dict[state] = color_dict[state]
                show_legend = True
            else:
                show_legend = False
            trace = go.Scattergl(
                # plot the incident begin date on the x-axis and the incident type on the y-axis
                x=df_selection[df_selection['state'] == state]['incident_begin_date'],
                y=df_selection[df_selection['state'] == state]['incident_type'],
                mode='markers',
                name=state,
                marker=dict(color=state_color_dict[state]),
                showlegend=show_legend,
                text='<br>Area: ' + df_selection['designated_area'] +
                '<br>Type: ' + df_selection['incident_type'] +
                '<br>Began: ' + pd.to_datetime(df_selection['incident_begin_date']).dt.strftime("%Y-%m-%d").fillna("N/A") +
                '<br>Ended: ' + pd.to_datetime(df_selection['incident_end_date']).dt.strftime('%Y-%m-%d').fillna("N/A"),#.apply(lambda x: x.strftime('%Y-%m-%d') if x is not None else 'N/A'),
                hovertemplate='<b>%{text}</b>'
            )
            # append the trace to the list of traces
            traces.append(trace)

    # create the figure with the list of traces and update the layout
    fig_scatter = go.Figure(data=traces)
    fig_scatter.update_layout(
        title='Incident Type by Year',
        xaxis_title='Year', yaxis_title='Incident Type',
        legend=dict(title='Color of State',))

    return fig_scatter

# ---- RENDER ----

def graphs(filter=defaultQuery):
  st.markdown("---")
  inc_freq_cont = st.container()
  inc_freq_cont.plotly_chart(incident_freq(filter), use_container_width=True)
  st.markdown("---")
  by_state_cont = st.container()
  by_state_cont.plotly_chart(incident_by_state(filter), use_container_width=True)

  st.markdown("---")
  scatter_row = st.container()
  scatter_row.plotly_chart(incident_type_year(filter), use_container_width=True)
  st.markdown("---")
  line_row = st.container()
  line_row.plotly_chart(incidents_per_year(filter), use_container_width=True)



def render_page(df):
  with st.spinner('Currently loading data...'):
    top_info(df)
    st.title('Visualizations')
    tab1, tab2, tab3, tab4 = st.tabs(["All 📈", "Flood 🌊", "Tornado 🌪️", "Custom ⚙️"])
    with tab1:
      graphs()
    with tab2:
      df_fire = df.query(f'state == {getSelection()} & incident_type == ["Flood"]')
      graphs(df_fire)
    with tab3:
      df_storms = df.query(f'state == {getSelection()} & incident_type == ["Tornado"]')
      graphs(df_storms)
    with tab4:
      filters(df)
      graphs(DF_SELECTION)

render_page(df_main)