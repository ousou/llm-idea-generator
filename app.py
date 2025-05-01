import streamlit as st
from google import genai
from google.genai import types

# Set up Google Gemini API
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]

# Model to use
MODEL_NAME = 'gemini-2.0-flash-001'

# Streamlit UI
st.title("LLM Discussion")

llm1_prompt = st.text_area("LLM 1 System Prompt", "You are a helpful assistant.")
llm2_prompt = st.text_area("LLM 2 System Prompt", "You are a knowledgeable expert.")
topic = st.text_input("Discussion Topic", "The future of AI")

if st.button("Start Discussion"):
    # Placeholder for LLM discussion logic
    st.write("Starting discussion...")

    # Initialize the generative model
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Function to get a response from the model
    def get_response(prompt, history=None):
        #generation_config = genai.GenerationConfig(
        #    temperature=0.5,
        #    top_p=1.0,
        #    top_k=1,
        #    max_output_tokens=2048,
        #)

        prompt_parts = [prompt]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_parts,
            # config=generation_config,
        )
        return response.text

    # Start the discussion
    llm1_response = get_response(llm1_prompt + "\\n\\n" + topic)
    llm2_response = get_response(llm2_prompt + "\\n\\n" + llm1_response)

    st.write("LLM 1:", llm1_response)
    st.write("LLM 2:", llm2_response)