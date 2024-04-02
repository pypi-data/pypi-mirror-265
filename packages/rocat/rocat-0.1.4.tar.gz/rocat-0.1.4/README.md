# RoCat: A Simple and User-Friendly Library for AI Services

RoCat is a Python library that provides a simple and user-friendly interface for integrating AI services into your projects.

## Installation

You can install RoCat using pip:

​```
pip install rocat
​```

## Usage

To use RoCat in your project, follow these steps:

1. Import the necessary modules from the RoCat library:

​```
from rocat import ChatbotModule, create_app, run_app
​```

2. Create an instance of the `ChatbotModule` with your OpenAI API key:

​```
api_key = "YOUR_API_KEY"
chatbot = ChatbotModule(api_key)
​```

3. Use the `generate_response` method to generate a response based on a user prompt:

​```
user_prompt = "What is the capital of France?"
response = chatbot.generate_response(user_prompt)
print(response)
​```

4. (Optional) If you want to customize the system prompt for the chatbot, use the `set_system_prompt` method:

​```
chatbot.set_system_prompt("You are a helpful travel assistant.")
​```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/yourusername/rocat).

## Acknowledgements

RoCat is built on top of the following libraries:
- [OpenAI](https://openai.com/) - API for AI services
- [Streamlit](https://streamlit.io/) - Framework for building web applications

## Contact

If you have any questions or inquiries, please contact the author:

- Name: Faith6
- Email: root@yumeta.kr
- GitHub: [Yumeta-Lab](https://github.com/Yumeta-Lab)