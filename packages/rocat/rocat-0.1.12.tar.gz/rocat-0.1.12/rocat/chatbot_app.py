# rocat/streamlit_app.py
import streamlit as st
from .chatbot_modules import Chatbot  

class ChatbotApp:
    def __init__(self, api_key, system_prompt="You are a helpful assistant."):
        self.chatbot = Chatbot(api_key)
        self.system_prompt = system_prompt
        self.chatbot.set_system_prompt(system_prompt)

    def create_app(self):
        st.title("RoCat AI Chatbot Test App")
        self.run_app()

    def run_app(self):
        user_prompt = st.text_input("User Input")
        if st.button("Generate Response"):
            response = self.chatbot.generate_response(user_prompt)
            st.write("Assistant:", response)