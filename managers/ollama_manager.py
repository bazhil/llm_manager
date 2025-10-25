import os
from ollama import Client
from ollama import ChatResponse
from dotenv import load_dotenv

from utils import extract_reasoning_text

load_dotenv()


class OllamaManager:
    """Manage the Ollama"""
    # https://github.com/ollama/ollama-python

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of Ollama client"""
        if cls._client is None:
            host = os.getenv('OLLAMA_HOST')
            if not host:
                raise ValueError("OLLAMA_HOST не установлен в переменных окружения")
            cls._client = Client(host=host)
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from the Ollama"""

        client = cls._get_client()
        response: ChatResponse = client.chat(
            model=os.getenv('OLLAMA_MODEL'),
            messages=[
                {"role": "assistant", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        result = extract_reasoning_text(response['message']['content'])

        return result