
import streamlit as st
from google import genai
from google.genai import types

# Set up Google Gemini API
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]

# Model to use
MODEL_NAME = 'gemini-2.0-flash-001'

import streamlit as st

# Streamlit UI
st.markdown("""
<style>
div.stTextArea textarea {
    background-color: #E0FFFF !important; /* Light Blue */
}
div.stTextInput input {
    background-color: #E0FFFF !important; /* Light Blue */
}
</style>
""", unsafe_allow_html=True)

st.title("LLM Discussion")

llm1_prompt = st.text_area("LLM 1 System Prompt", "You are a human in conversation with another human. You are a novice who wants to learn about the topic at hand. You ask questions about things you don't grasp.")
llm2_prompt = st.text_area("LLM 2 System Prompt", "You are a human in conversation with another human. You are a knowledgeable expert giving concise answers to questions, and probe with clarifying questions to check the understanding of the other person when needed.")
topic = st.text_input("Discussion Topic", "The future of AI")

import asyncio

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the generative model
client = genai.Client(api_key=GOOGLE_API_KEY)

# Function to get a response from the model
def get_response(prompt, history=""):
    #generation_config = genai.GenerationConfig(
    #    temperature=0.5,
    #    top_p=1.0,
    #    top_k=1,
    #    max_output_tokens=2048,
    #)

    prompt_parts = [prompt + "\\n\\n" + history]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_parts,
        # config=generation_config,
    )
    return response.text

async def llm1_turn(topic):
    history = f"The discussion topic is: {topic}\\n"
    for chat in st.session_state.chat_history:
        history += chat["speaker"] + ": " + chat["message"] + "\\n"
    llm1_response = get_response(llm1_prompt, history)
    st.session_state.chat_history.append({"speaker": "LLM 1", "message": llm1_response})

async def llm2_turn(topic):
    history = f"The discussion topic is: {topic}\\n"
    for chat in st.session_state.chat_history:
        history += chat["speaker"] + ": " + chat["message"] + "\\n"
    llm2_response = get_response(llm2_prompt, history)
    st.session_state.chat_history.append({"speaker": "LLM 2", "message": llm2_response})

# Display chat history

def display_chat_history():
    with chat_placeholder.container():
        message_counter = 0
        for chat in st.session_state.chat_history:
            if message_counter % 2 == 0:
                st.write(f'<div style="text-align: left; padding-left: 300px; background-color:#f0f2f5;padding:10px;border-radius:5px;">{chat["speaker"]}: {chat["message"]}</div>', unsafe_allow_html=True)
            else:
                st.write(f'<div style="text-align: right; padding-right: 300px; background-color:#e2e3e5;padding:10px;border-radius:5px;">{chat["speaker"]}: {chat["message"]}</div>', unsafe_allow_html=True)
                message_counter += 1
chat_placeholder = st.empty()
if st.button("Go!"):
    display_chat_history()
    if st.session_state.chat_history:
        last_llm2_response = st.session_state.chat_history[-1]["message"]
        with st.spinner("LLM 1 is generating a response..."):
            asyncio.run(llm1_turn(topic))
    else:
        with st.spinner("LLM 1 is generating a response..."):
            asyncio.run(llm1_turn(topic))
    with st.spinner("LLM 2 is generating a response..."):
        asyncio.run(llm2_turn(topic))
    display_chat_history()