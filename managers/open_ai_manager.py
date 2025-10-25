import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIManager:
    """Manage the OpenAI API"""

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of OpenAI client"""
        if cls._client is None:
            # OpenAI клиент сам проверит OPENAI_API_KEY из переменных окружения
            cls._client = OpenAI()
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str,prompt: str):
        """Get response from the OpenAI"""

        client = cls._get_client()
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )

        if response:
            return response.choices[0].message.content
        else:
            return "Error in generating response."
