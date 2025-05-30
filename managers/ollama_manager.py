import os
from ollama import Client
from ollama import ChatResponse
from dotenv import load_dotenv

from utils import extract_reasoning_text

load_dotenv()


class OllamaManager:
    """Manage the Ollama"""
    # https://github.com/ollama/ollama-python

    client = Client(
        host=os.getenv('OLLAMA_HOST'),
    )

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from the Ollama"""

        response: ChatResponse = cls.client.chat(
            model=os.getenv('OLLAMA_MODEL'),
            messages=[
                {"role": "assistant", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        result = extract_reasoning_text(response['message']['content'])

        return result