# rocat/chatbot.py
from openai import OpenAI

class Chatbot:
    def __init__(self, api_key):
        """Initialize the chatbot with the given API key."""
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
        self.system_prompt = "You are a helpful assistant."

    def set_system_prompt(self, new_prompt):
        """Set the system prompt for the chatbot."""
        self.system_prompt = new_prompt

    def generate_response(self, user_prompt):
        """Generate a response based on the given user prompt."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()