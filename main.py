import os
# from constant import openai_key  # Ensure you have this constant defined with your OpenAI key
# from langchain.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import chainlit as cl

# Set the OpenAI API key
# os.environ["OPENAI_API_KEY"] = openai_key

# Initialize the LLM model (use OpenAI if you need, here shown with ChatGroq as per your initial code)
llm = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

# Define the Chainlit message handler
@cl.on_message
async def main(message: cl.Message):
    system_message = "You are a helpful assistant."
    human_message = message.content

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])

    chain = prompt | llm

    # Generate the response using the LLM
    response = chain.invoke({"text": human_message})
    print(response)
    print('Type: ',type(response))
    # Send a response back to the user
    await cl.Message(
        content=f"Bot: {response.__dict__['content']}",
    ).send()

# Ensure you run Chainlit with proper configuration, usually by running `chainlit run <script_name>.py`