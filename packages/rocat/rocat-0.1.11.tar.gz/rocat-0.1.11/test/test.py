# main.py
import rocat as rc

def main():
    api_key = "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"
    system_prompt = "너는 지금부터 류동윤이다."
    app = rc.ChatbotApp(api_key, system_prompt)
    app.create_app()

if __name__ == "__main__":
    main()