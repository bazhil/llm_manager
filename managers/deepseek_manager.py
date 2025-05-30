import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class DeepSeekManager:
    """Manage the Deepseek API"""

    client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the Deepseek"""

        response = cls.client.chat.completions.create(
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
