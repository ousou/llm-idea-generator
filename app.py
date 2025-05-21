import streamlit as st
from google import genai
import asyncio


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

st.title("LLM Idea Generator")

idea_generator_prompt = st.text_area("Idea Generator System Prompt", "You generate an idea on the given topic, and refine it based on the feedback from the other person. Be concise, though give more details if the counterpart ask for them.")
idea_critic_prompt = st.text_area("Idea Critic System Prompt", "You critique ideas given by your counterpart and score them from 0 to 10. Give clear and actionable feedback. Be concise. Be very critical! Question all parts of the idea.")
topic = st.text_area("What to generate ideas on?", "A fun thing to do with friends on the weekend.")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the generative model
if st.secrets["gemini"].get("vertexai", False):
    client = genai.Client(
        project="iprally-ai-dev",
        location="global",
        vertexai=True,
    )
elif st.secrets["gemini"].get("api_key"):
    client = genai.Client(api_key=st.secrets["gemini"].get("api_key"))
else:
    raise ValueError("No API key or vertexai credentials provided in secrets.toml")

# Model to use
MODEL_NAME = st.secrets["gemini"].get("model", "gemini-2.0-flash-001")



# Function to get a response from the model
def get_response(prompt, history=""):
    prompt_parts = [prompt + "\\n\\n" + history]
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_parts,
        # config=generation_config,
    )
    return response.text

async def idea_generator_response(topic):
    history = f"The task is: {topic}\\n"
    for chat in st.session_state.chat_history:
        history += chat["speaker"] + ": " + chat["message"] + "\\n"
    llm1_response = get_response(idea_generator_prompt, history)
    st.session_state.chat_history.append({"speaker": "Ideator", "message": llm1_response})

async def idea_critic_response(topic):
    history = f"The task is: {topic}\\n"
    for chat in st.session_state.chat_history:
        history += chat["speaker"] + ": " + chat["message"] + "\\n"
    llm2_response = get_response(idea_critic_prompt, history)
    st.session_state.chat_history.append({"speaker": "Critic", "message": llm2_response})

# Display chat history

def display_chat_history():
    with chat_placeholder.container():
        message_counter = 0
        for chat in st.session_state.chat_history:
            if message_counter % 2 == 0:
                st.write(f'<div style="padding-left: 300px; background-color:#f0f2f5;padding:10px;border-radius:5px;"><strong><em>{chat["speaker"]}</em></strong>: {chat["message"]}</div>', unsafe_allow_html=True)
            else:
                st.write(f'<div style="padding-right: 300px; background-color:#e2e3e5;padding:10px;border-radius:5px;"><strong><em>{chat["speaker"]}</em></strong>: {chat["message"]}</div>', unsafe_allow_html=True)
            message_counter += 1
chat_placeholder = st.empty()
if st.button("Go!"):
    display_chat_history()
    with st.spinner("Idea Generator is generating a response..."):
        asyncio.run(idea_generator_response(topic))
    with st.spinner("Idea Critic is generating a response..."):
        asyncio.run(idea_critic_response(topic))
    display_chat_history()