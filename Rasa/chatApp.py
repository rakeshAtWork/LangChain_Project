import streamlit as st
import requests
import base64
import time

img_path = r"logo2.png"

# Function to send a message to the Rasa bot
def send_message(message):
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook', 
        json={"sender": "user", "message": message}
    )
    return response.json()

# Load the binary of the logo data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode() 

# Streamlit UI
# Add CSS for fixed header
 
# Main content with padding
st.set_page_config(page_title="CozBot", page_icon=":robot_face:")

img_base64 = get_base64_of_bin_file(img_path)

# Streamed response emulator : this function used for the stream output functionality.
def response_generator(res):
    for word in res.split():
        yield word + " "
        time.sleep(0.03)
        
# Add CSS for fixed header
st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 20px;
        width: 50%;
        background-color: white;
        z-index: 999991;
        /*padding:30px 10px;*/
        box-shadow: 0 ;
    }
    .main-content {
        padding-top: 50px;
        z-index: 1; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fixed title with logo
st.markdown(
    f'<div class="fixed-title"><img src="data:image/png;base64,{img_base64}" style="height: 50px; margin-right: 10px;"></div>',
    unsafe_allow_html=True
)

# Main content with padding
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and responses
if user_input := st.chat_input("Hello?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    print(user_input)

    with st.spinner('Thinking ...'):
        try:
            response = send_message(user_input)
        except:
            response = "Unable to connect with the CozBot Server. Please try later."

    print(response)
    with st.chat_message("assistant"):
        if len(response) !=0:
            try:
                res1=response[0]['text']
            except:
                res1 = "Unable to connect with the CozBot Server. Please try later."
                print("Not able to retvie data due to bad index")
            st.write_stream(response_generator(res1))
            st.session_state.messages.append({"role": "assistant", "content": res1})
        else:
       
            st.write_stream(response_generator("Didn't Understand. Ask Something else?.."))
            # st.session_state.messages.append("..")        

st.markdown('</div>', unsafe_allow_html=True)
