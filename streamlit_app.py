import streamlit as st
import requests
import uuid
import json
from typing import List, Dict

# Hide Streamlit menu and footer
st.set_page_config(
    page_title="Chat Interface",
    menu_items={},  # Empty dict removes all menu items
    initial_sidebar_state="collapsed"
)

# Hide hamburger menu and "deploy" button with more specific selectors
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="stDecoration"] {visibility: hidden !important;}
        [data-testid="stHeader"] {visibility: hidden !important;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Constants
WEBHOOK_URL = "https://n8n-a48r.onrender.com/webhook/invoke_agent"  # Replace with your webhook URL
BEARER_TOKEN = "teste01"     # Replace with your bearer token
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display all messages in the chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.messages.append({"role": role, "content": content})

def send_message_to_webhook(session_id: str, user_input: str) -> Dict:
    """Send message to webhook and return response"""
    payload = {
        "sessionId": session_id,
        "chatInput": user_input
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with webhook: {str(e)}")
        return {"output": "Sorry, I encountered an error processing your request."}

def main():
    st.title("Como analista especializado, reviso e otimizo anúncios imobiliários para portais portugueses (Idealista, Imovirtual, Supercasa e Casayes). Analiso o anúncio original, identifico melhorias e oportunidades para aumentar a atratividade, focando em captar a atenção do público-alvo e alinhando com as melhores práticas do mercado.")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat
        add_message("user", user_input)
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_to_webhook(
                    st.session_state.session_id,
                    user_input
                )
                bot_response = response.get("output", "Sorry, I couldn't process your request.")
                st.write(bot_response)
                add_message("assistant", bot_response)

if __name__ == "__main__":
    main()