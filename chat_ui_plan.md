# Plan for Implementing a Real-Time Conversational UI

This plan outlines the steps to modify `app.py` to create a real-time, conversational user interface where user and AI messages appear sequentially in a single, continuous column, mimicking a natural chat flow.

## Goals

*   Implement a chat history to store the conversation.
*   Display the chat history with distinct styling for different speakers.
*   Update the chat history in real-time as new messages are generated.
*   Enable asynchronous message generation for a fluid interaction.
*   Allow the user to input messages and participate in the conversation.

## Steps

1.  **Implement a Chat History:** Store the conversation history in a list. Each item in the list will be a dictionary containing the speaker (user, LLM1, LLM2) and the message.
2.  **Display the Chat History:** Iterate through the chat history and display each message. Use Streamlit's `st.markdown` to format the messages with different background colors or styles to differentiate between speakers.
3.  **Real-time Updates:** Use `st.empty()` to create a placeholder for the chat history. After each message is generated, update the placeholder with the new chat history.
4.  **Asynchronous Message Generation:** Use `asyncio` to generate messages from LLM1 and LLM2 concurrently, allowing for a more fluid interaction.
5.  **User Input:** Add a text input field for the user to send messages. Append the user's message to the chat history and trigger the LLM responses.

## Mermaid Diagram

```mermaid
sequenceDiagram
 participant User
 participant Streamlit App
 participant LLM1
 participant LLM2

 User->>Streamlit App: Enters message
 Streamlit App->>Streamlit App: Appends message to chat history
 Streamlit App->>LLM1: Sends prompt (user message + LLM1 prompt)
 activate LLM1
 LLM1-->>Streamlit App: Returns LLM1 response
 deactivate LLM1
 Streamlit App->>Streamlit App: Appends LLM1 response to chat history
 Streamlit App->>LLM2: Sends prompt (LLM1 response + LLM2 prompt)
 activate LLM2
 LLM2-->>Streamlit App: Returns LLM2 response
 deactivate LLM2
 Streamlit App->>Streamlit App: Appends LLM2 response to chat history
 Streamlit App->>User: Updates chat history display