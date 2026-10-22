import os
import streamlit as st
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Constants
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"

# Streamlit Page Configuration
st.set_page_config(page_title="AI Agent Chat", page_icon="🤖", layout="wide")

# Initialize OpenAI Client
@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Missing GROQ_API_KEY in environment or .env file.")
        st.stop()
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

client = get_client()

# --- Sidebar Layout & Usability ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown(f"**Current Model:** `{DEFAULT_MODEL}`")
    
    # Feature: Clear Chat History button
    if st.button("🗑️ Clear Chat History"):
        # Reset the session state
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful and friendly AI assistant."}
        ]
        st.success("Chat history cleared!")

# --- Main UI Layout ---
st.title("🤖 AI Agent Chatbot")
st.markdown("Welcome to the enhanced Web Interface. **Try asking a question below!**")

# Initialize session state for chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and friendly AI assistant."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input with improved placeholder (UX guideline)
prompt = st.chat_input("Type your message…")

# --- Input Validation ---
# Ensure prompt is not None and not just empty whitespace
if prompt is not None and prompt.strip():
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # UX Feature: "Thinking…" state before API resolves
        message_placeholder.markdown("Thinking…")
        
        full_response = ""
        try:
            # Query the LLM
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=st.session_state.messages,
                temperature=0.7,
            )
            full_response = response.choices[0].message.content or ""
            
            # Replace the "Thinking…" text with the actual response
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Graceful error handling (Toast + Inline error)
            error_msg = f"Sorry, I encountered a network error: {e}"
            message_placeholder.error(error_msg)
            st.toast("Failed to connect to the API.", icon="⚠️")
