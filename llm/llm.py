import ollama

from config import MODEL_NAME, TEMPERATURE


class LLM:

    def __init__(self):
        self.model = MODEL_NAME

    def generate(self, prompt):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": TEMPERATURE
            }
        )
        print("\nLLM Response:")
        print(response)
        return response["message"]["content"]