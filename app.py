import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly
import streamlit as st  # pip install streamlit
import datetime
import plotly.graph_objects as go

# Streamlit Documentation: https://docs.streamlit.io/
# Plotly: https://plotly.com/python/
# Pandas: https://www.w3schools.com/python/pandas/default.asp

st.set_page_config(page_title="NDD",
                   page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data():
  # ---- READ CSV ----
    df = pd.read_csv('us_disasters_m5.csv')
    # Should return the year, ie 2017
    df["year"] = pd.to_datetime(df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.year
    # Should return the date, ie 2011-02-27
    df["date"] = pd.to_datetime(df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.date
    return df
df = get_data()

# ---- SIDEBAR ----
st.sidebar.header("Filter Selections")

state = st.sidebar.multiselect(
    "State Selections",
    options=df["state"].unique(),
    default=df["state"].unique()

)

incident_type = st.sidebar.multiselect(
    "Incident Selections",
    options=df["incident_type"].unique(),
    default=df["incident_type"].unique()

)

st.sidebar.header("Features In Progress")
start_year = st.sidebar.date_input("Select Start Date", datetime.date(2011, 1, 1))
end_year = st.sidebar.date_input("Select End Date")

# Provides results to graphs for active filters
df_selection = df.query(
    "state == @state & incident_type == @incident_type"
)

# Future use for AI Button
askBot = st.sidebar.button("Ask DisasterBot", use_container_width=True)
if askBot:
    st.sidebar.info('This feature is coming soon.', icon="ℹ️")

st.sidebar.write(':tea: SDEV-282 Prototype by Joe A. and Aaron C.')

# ---- MAINPAGE ----
st.title(":bar_chart: Natural Disaster Dashboard")
st.markdown("##")

# Top portion for totals
st.title('Disaster Totals')
total_incidents = int(df["incident_type"].count())
total_states = df['state'].nunique()

left_column, right_column, blank_column2 = st.columns(3)

with left_column:
    st.subheader(f"Total Incidents: :red[{total_incidents}]")
with right_column:
    st.subheader(f"Total States: :blue[{total_states}]")
with blank_column2:
    st.empty()

st.markdown("---")

# Total Incidents in each State [BAR CHART]
incidents_by_state = (
    df_selection.groupby(by=["state"]).count()[["incident_type"]].sort_values(
      by="incident_type")
)


fig_incidents_by_state = px.bar(incidents_by_state, y=incidents_by_state.index,
                  x="incident_type", labels={"incident_type": "No. Incidents", "state": "State"}, color=incidents_by_state.index, title="Total Incidents in each State")


fig_incidents_by_state.update_layout(yaxis=dict(autorange="reversed")) #Sorts Bar Chart

# Incident Frequency [BAR CHART]
incident_frequency = df_selection.groupby(by=["incident_type"]).count()[
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

# Number of incidents per year [LINE GRAPH]
incidents_by_year = df_selection #Not used currently, use events_per_date instead
events_per_date = df_selection.groupby('year').size().reset_index(name='events_count')

fig_year = px.line(events_per_date, x="year", y='events_count', title="Incidents by Year")

left_column, right_column = st.columns(2, gap='large')
left_column.plotly_chart(fig_incident_frequency, use_container_width=True)
right_column.plotly_chart(fig_incidents_by_state, use_container_width=True)

# Incident types by year [SCATTER GRAPH]
fig_scatter = go.Figure(data=go.Scattergl(
    x = df_selection['incident_begin_date'],
    y = df_selection['incident_type'],
    text = 'State: ' + df_selection['state'] +
            '<br>Area: ' + df_selection['designated_area'] +
            '<br>Title: ' + df_selection['declaration_title'] +
            '<br>Type: ' + df_selection['incident_type'] +
            '<br>Begun: ' + df_selection['incident_begin_date'] +
            '<br>Ended: ' + df_selection['incident_end_date'],
    mode='markers',
    hovertemplate='%{text}'
))
fig_scatter.update_layout(title='Incident Type by Year', xaxis_title='Year', yaxis_title='Event')

st.markdown("---")
bottom_row = st.container()
bottom_row.plotly_chart(fig_year, use_container_width=True)

st.markdown("---")
scatter_row = st.container()
scatter_row.plotly_chart(fig_scatter, use_container_width=True)


# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)
