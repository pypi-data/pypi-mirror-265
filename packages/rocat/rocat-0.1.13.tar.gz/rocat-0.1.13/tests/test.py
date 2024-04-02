import anthropic

client = anthropic.Anthropic(
    api_key="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",
)

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0.0,
    system="Respond only in Yoda-speak.",
    messages=[
        {"role": "user", "content": "How are you today?"}
    ]
)

print(message.content[0].text)