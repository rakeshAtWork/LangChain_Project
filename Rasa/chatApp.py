import streamlit as st
import requests
import base64

img_path = r"logo2.png"

# Streamlit interface


# Function to send a message to the Rasa bot
def send_message(message):
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook', 
        json={"sender": "user", "message": message}
    )
    return response.json()

# # Text input for the user
# user_message = st.text_input("You: ", "")

# # Display bot response
# if st.button("Send"):
#     if user_message:
#         response = send_message(user_message)
#         if response:
#             for res in response:
#                 st.text(f"Bot: {res['text']}")
#         else:
#             st.text("Bot: No response received")



# Our Running Code :

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode() 

# Streamlit UI
# Add CSS for fixed header
 
# Main content with padding
st.set_page_config(page_title="CozBot", page_icon=":robot_face:")

img_base64 = get_base64_of_bin_file(img_path)

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
        response = send_message(user_input)

    print(response)
    with st.chat_message("assistant"):
        if len(response) !=0:
        
            st.markdown(response[0]['text'])
            st.session_state.messages.append({"role": "assistant", "content": response[0]['text']})
        else:
       
            st.markdown("Didn't Understand. Ask Something else?..")
            # st.session_state.messages.append("..")        

st.markdown('</div>', unsafe_allow_html=True)
