import streamlit as st
import time
import os
import sys

# --- Path Setup ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.agents.whatsapp_sim_agent import WhatsAppFinanceBot

# --- CUSTOM CSS FOR WHATSAPP LOOK ---
st.markdown("""
<style>
    .stApp {
        background-color: #E5DDD5;
        background-image: url("https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png");
        background-repeat: repeat;
    }
    .chat-container {
        max-width: 600px;
        margin: auto;
    }
    /* Messages */
    .stChatMessage {
        background-color: transparent !important;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        /* User Message (Right) */
        flex-direction: row-reverse;
        background-color: #dcf8c6 !important;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        color: black;
    }
    
    /* We can't fully target specific bubbles easily in pure Streamlit Markdown, 
       so we rely on standard chat behavior but adding a header */
    
    .whatsapp-header {
        background-color: #075E54;
        color: white;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .whatsapp-title {
        font-weight: bold;
        font-size: 18px;
        margin-left: 10px;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="whatsapp-header">
    <div class="avatar" style="background-image: url('https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg'); background-size: cover;"></div>
    <div class="whatsapp-title">Inandes Finance Bot (Simulador)</div>
</div>
""", unsafe_allow_html=True)

# --- INIT STATE ---
if "wa_bot_engine" not in st.session_state:
    st.session_state.wa_bot_engine = WhatsAppFinanceBot()
if "wa_session_state" not in st.session_state:
    st.session_state.wa_session_state = {'step': 'INIT', 'user_data': {}}
if "wa_messages" not in st.session_state:
    # Initial Greeting
    initial_msg, new_state = st.session_state.wa_bot_engine.process_message(
        {'step': 'INIT'}, ""
    )
    st.session_state.wa_messages = [{"role": "assistant", "content": initial_msg}]
    st.session_state.wa_session_state = new_state

# --- DISPLAY CHAT ---
for msg in st.session_state.wa_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT ---
if prompt := st.chat_input("Escribe un mensaje..."):
    # 1. Add User Message
    st.session_state.wa_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Process Logic
    bot = st.session_state.wa_bot_engine
    current_state = st.session_state.wa_session_state
    
    # Simulate thinking time
    with st.spinner("Escribiendo..."):
        time.sleep(0.8)
        
    response_text, next_state = bot.process_message(current_state, prompt)
    
    # 3. Add Bot Response
    st.session_state.wa_session_state = next_state
    st.session_state.wa_messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
    
    # If returned to INIT (e.g. exit), maybe clear history? 
    # Optional: Keep history for demo effect.

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("🔧 Debug / Info")
    st.write(f"**Estado Actual:** {st.session_state.wa_session_state.get('step')}")
    st.markdown("---")
    st.info("Datos de Prueba:")
    st.code("DNI: 70559385\nClave: 1234")
    st.markdown("---")
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", width=50)
    st.caption("Simulación Local de WhatsApp API")
