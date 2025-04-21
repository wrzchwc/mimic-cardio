from openai import OpenAI
from openai.types.responses import Response

def query_model(prompt: str, model: str = "gpt-4.1-nano") -> Response:
    client = OpenAI()
    return client.responses.create(
        model=model,
        input=prompt
    )