import streamlit as st
import numpy as np
from fetch_augment import final_result
# Streamlit UI
# Add CSS for fixed header

# Main content with padding
st.set_page_config(page_title="CozBot", page_icon=":robot_face:")

# Add CSS for fixed header
st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 0;
        width: 50%;
        background-color: white;
        z-index: 100;
        padding:30px 10px;
        box-shadow: 0 ;
    }
    .main-content {
        padding-top: 50px;
    }
    body {
        background-image: url('https://www.cozentus.com/uploads/images/home-banner-1-2.webp');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fixed title
st.markdown('<div class="fixed-title"><h1>CozBot</h1></div>', unsafe_allow_html=True)

# Main content with padding
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and responses
if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    print(user_input)

    response = final_result(user_input)

    with st.chat_message("assistant"):
        st.markdown(response['result'])
        st.session_state.messages.append({"role": "assistant", "content": response['result']})
    print(response['result'])

st.markdown('</div>', unsafe_allow_html=True)