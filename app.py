import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Natural Disasters Dashboard",
                   page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_excel():
  # ---- READ CSV ----
    df = pd.read_csv('us_disasters_m5.csv')
    df["year"] = pd.to_datetime(df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.year
    df["date"] = pd.to_datetime(df["incident_begin_date"], format="%Y-%m-%d", exact=False).dt.date
    return df


df = get_data_from_excel()

st.sidebar.header("Filter Selection")
state = st.sidebar.multiselect(
    "Select the State",
    options=df["state"].unique(),
    default=df["state"].unique()

)

incident_type = st.sidebar.multiselect(
    "Select the Incident Type",
    options=df["incident_type"].unique(),
    default=df["incident_type"].unique()

)

df_selection = df.query(
    "state == @state & incident_type == @incident_type"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Natural Disaster Dashboard")
st.markdown("##")

# Top portion for totals
total_incidents = int(df["incident_type"].count())
total_states = df['state'].nunique()

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Incidents:")
    st.subheader(f"{total_incidents}")
with right_column:
    st.subheader("Total States:")
    st.subheader(f"{total_states}")

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
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#Year Graph
incidents_by_year = df_selection

events_per_date = df_selection.groupby('year').size().reset_index(name='events_count')

fig_year = px.line(events_per_date, x="year", y='events_count', title="Incidents by Year")

left_column, right_column = st.columns(2, gap='large')
left_column.plotly_chart(fig_incident_frequency, use_container_width=True)
right_column.plotly_chart(fig_incidents_by_state, use_container_width=True)

st.markdown("---")

bottom_row = st.container()
bottom_row.plotly_chart(fig_year, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
