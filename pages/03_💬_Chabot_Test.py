import streamlit as st
import openai
from streamlit_chat import message
import os

st.set_page_config(page_title="NDD - Chatbot",
                   page_icon="💬", layout="wide")

st.title("💬 Chat with DisasterBot")

try:
  openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
  st.write("API KEY was not found!")

# default_text = 'Please enter a question for the chatbot.'
# # userInput = 'This is sample user input.'
# userInputTest = st.text_input('User Input for Chatbot', default_text)
# # userInputTest = st.text_area('User Input for Chatbot', default_text)
# botOutput = 'This is sample chatbot output.'

# if userInputTest != default_text:
#   message(userInputTest, is_user=True)
#   message(botOutput)

def generate_response(prompt):
  completions = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    max_tokens = 100, #Limited for testing
    n = 1,
    stop = None,
    temperature=0.5,
  )
  message = completions.choices[0].text
  return message

# Storing Chat Information
if 'generated' not in st.session_state:
  st.session_state['generated'] = []

if 'past' not in st.session_state:
  st.session_state['past'] = []

def get_text():
  input_text = st.text_input("You: ", key="input")
  return input_text

user_input = get_text()

if user_input:
  output = generate_response(user_input)
  # Store the output
  st.session_state.past.append(user_input)
  st.session_state.generated.append(output)

# Display Chat History
if st.session_state['generated']:

  for i in range(len(st.session_state['generated']) -1, -1, -1):
    message(st.session_state['generated'][i], key=str(i))
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

# ---- STREAMLIT STYLE ----
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True)