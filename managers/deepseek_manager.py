import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class DeepSeekManager:
    """Manage the Deepseek API"""

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of DeepSeek client"""
        if cls._client is None:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY не установлен в переменных окружения")
            cls._client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the Deepseek"""

        client = cls._get_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        if response:
            return response.choices[0].message.content
        else:
            return "Error in generating response."
