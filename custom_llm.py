import openai

client = openai.OpenAI(
    api_key='')


class GPT4LLM:
    def __init__(self, api_key):
        client.api_key = api_key

    def generate_action(self, messages):
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            ai_response = chat_completion.choices[0].message.content
            return ai_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
