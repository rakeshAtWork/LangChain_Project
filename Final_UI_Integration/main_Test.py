import streamlit as st
from openai import OpenAI

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh;">
        <h1 style="font-family: Arial, sans-serif; font-size: 48px; font-weight: bold;">CozBot</h1>
    </div>
    """,
    unsafe_allow_html=True
)


client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="shenzhi-wang/Llama3-8B-Chinese-Chat-GGUF-8bit",
  messages=[
    {"role": "system", "content": "Always answer to the point"},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.7,
)



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        
        response = completion.choices[0].message
        st.markdown(response)
        
        # for line in response.splitlines():
        #     st.markdown(line)
        #     # Optional delay for dramatic effect
        #     time.sleep(0.2)
        

    st.session_state.messages.append({"role": "assistant", "content": response})