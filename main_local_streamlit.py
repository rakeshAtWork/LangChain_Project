import os
# from constant import openai_key  # Ensure you have this constant defined with your OpenAI key
# from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import chainlit as cl

# Set the OpenAI API key
# os.envirn["OPENAI_API_KEY"] = openai_key

# Initialize the LLM model (use OpenAI if you need, here shown with ChatGroq as per your initial code)
llm = Ollama(model = "llama3")
output_parser=StrOutputParser()

# Define the Chainlit message handler
@cl.on_message
async def main(message: cl.Message):
    system_message = "You are a helpful assistant."
    human_message = message.content

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])

    chain = prompt|llm|output_parser

    # Generate the response using the LLM
    response = chain.invoke({"text": human_message})
    print(response)
    print('Type: ',type(response))
    elements = [
        cl.Text(name="Response", content=response, display="inline")
    ]

    # Send a response back to the user
    await cl.Message(
        content=f"Bot: {response}",
        elements=elements
    ).send()
 
# @cl.on_chat_start
# async def start():
#     # text_content = "Hello, this is a text element."
 
#     await cl.Message(
#         content="Check out this text element!",
#         elements=elements,
#     ).send()
# # Ensure you run Chainlit with proper configuration, usually by running `chainlit run <script_name>.py`