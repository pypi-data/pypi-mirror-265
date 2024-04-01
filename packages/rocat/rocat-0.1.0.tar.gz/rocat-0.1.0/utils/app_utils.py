# rocat/utils/app_util.py

import streamlit as st
from .api_utils import get_api_key, set_api_key

def create_app():
    st.title("RoCat AI Chatbot Test App")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        set_api_key(api_key)
    return api_key

def run_app(chatbot):
    user_prompt = st.text_input("User Input")
    if st.button("Generate Response"):
        if get_api_key():
            response = chatbot.generate_response(user_prompt)
            st.write("Assistant:", response)
        else:
            st.error("Please enter your OpenAI API Key.")