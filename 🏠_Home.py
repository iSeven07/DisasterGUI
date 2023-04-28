import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="NDD - Home",
                   page_icon="🏠", layout="wide")
add_logo("images/lrw-color.png")

with st.container():
    one_col, two_col = st.columns((1,2))
    one_col.image('images/logo-main.png', use_column_width=True)
    with two_col:
        st.subheader("Landslide Remediation Worldwide")
        st.write("Data that saves lives")

st.markdown('---')

with st.expander('About this application'):
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("https://cdn-images-1.medium.com/max/906/1*dVSDol9pouoO9IX_E_-35Q.png")

        with text_col:
            st.subheader("A Multi-page Interactive Dashboard with Streamlit and Plotly")
            st.write("""
                Our team chose to use Streamlit alongside Plotly and a few other tools to create this interactive data analysis dashboard. These tools allow us to create the lovely pages and graphs you are looking at right now.
                """)
            st.markdown("[Filler Link](https://google.com)")

    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("https://cdn-images-1.medium.com/max/906/1*hjhCIWGgLzOznTFwDyeIeA.png")

        with text_col:
            st.subheader("This dashboard will see integration with AI")
            st.write("""
                One thing our team prides itself on is our creativeness. We will be working hard throughout the next weeks to integrate AI into this data analysis tool. Keep a lookout for future updates!
                """)
            st.markdown("[Filler Link](https://google.com)")

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)