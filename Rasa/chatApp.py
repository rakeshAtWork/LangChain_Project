import streamlit as st
import requests

# Define the Rasa server endpoint
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

# Function to get response from Rasa server
def get_response_from_rasa(message):
    payload = {
        "sender": "user",  # You can set a unique sender id
        "message": message
    }
    response = requests.post(RASA_SERVER_URL, json=payload)
    return response.json()

# Streamlit UI
st.title("Chatbot with Rasa and Streamlit")

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You: ", key="user_input")

if user_input:
    # Append the user input to the conversation
    st.session_state.conversation.append(f"You: {user_input}")

    # Get the response from Rasa
    response = get_response_from_rasa(user_input)
    for res in response:
        st.session_state.conversation.append(f"Bot: {res['text']}")

    # Clear the input box
    st.text_input("You: ", value="", key="user_input")

# Display the conversation history
for chat in st.session_state.conversation:
    st.write(chat)
