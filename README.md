# 5/2 Tuesday Session Notes

## Dashboard Wide
➕ Swap to full dataset, away from m5<br>
➕ Add DisasterBot button to all pages<br>
➕ Add st.spinner to all pages (See Crime Data page for example)<br>
➕➕ Filter data down to only columns needed<br>

## Home
➕ Add Quick Glance<br>
  〰️ Incorporate Crime data into Quick Glance
  〰️ Swap Totals to averages of all data?
    〰️ Average incidents over Summer/Winter/Spring/Fall
➕➕ Choropleth Graph showing All Data<br>
  〰️ average number of events per county
  〰️ overlapping of data, aka disasters underneath crime
➕➕ Have filter for States or Regions / Date ranges that affects entire dashboard<br>
  〰️ STRETCH --> Store session_state in cookies
    〰️ https://pypi.org/project/extra-streamlit-components/

## Dashboard
➖ Remove Quick Glance<br>
➕➖ Change line graph to a log scale / exponential growth<br>
  〰️ https://plotly.com/python/log-plot/
  〰️ ```fig = px.scatter(df, x="gdpPercap", y="lifeExp", hover_name="country", log_y=True)```
    〰️ log_y can be swapped for log_x

## Location Data
➕➕ Animated choropleth graph with NOAA location data by weekly/monthly time values<br>
  〰️ Filter data by date, 2010 and on
    〰️ Count per fips code as fall back if too much data
      〰️ STRETCH --> Animated choropleth graph with NOAA data that has scatter plot of crime data on top of location data by weekly/monthly time values
    ➖ Remove NOAA Scatter plot graph

## Crime Data
❓ Violent Crime as Separate Map / Another Disaster on Dashboard Page<br>
➕➕ Filter Data Down to those 88 incidents in association with a declaration of disaster<br>

## Stretch Goals
➕ Integrate database<br>
➕ onClick() functionality to graphs<br>
  〰️🔗 https://plotly.com/python/click-events/
  〰️ Not entirely sure what we would do with this?
  〰️ Put into session data, and watch for changes to said session data.

