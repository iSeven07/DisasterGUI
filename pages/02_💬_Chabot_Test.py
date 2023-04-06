import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="NDD - Chatbot",
                   page_icon="💬", layout="wide")

st.title("💬 streamlit_chat test 1")

default_text = 'Please enter a question for the chatbot.'
# userInput = 'This is sample user input.'
userInputTest = st.text_input('User Input for Chatbot', default_text)
# userInputTest = st.text_area('User Input for Chatbot', default_text)
botOutput = 'This is sample chatbot output.'

if userInputTest != default_text:
  message(userInputTest, is_user=True)
  message(botOutput)

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)