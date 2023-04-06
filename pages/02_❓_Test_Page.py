import streamlit as st

st.title(":bar_chart: Disaster Dashboard 1")

st.write('Do Lorem aute quis excepteur occaecat amet anim in reprehenderit consectetur labore ad. Officia incididunt deserunt pariatur dolor aliquip aliquip enim ad commodo tempor velit veniam incididunt. Ullamco qui laboris ut dolore consequat commodo ad voluptate eiusmod. Non laboris nostrud labore pariatur duis occaecat sunt anim ex commodo. Anim dolore officia laboris aliqua ipsum laboris nulla aliquip. Voluptate officia consectetur nisi quis.')

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)