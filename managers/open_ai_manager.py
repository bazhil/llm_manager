from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIManager:
    """Manage the OpenAI API"""

    client = OpenAI()

    @classmethod
    async def get_response(cls, system_prompt: str,prompt: str):
        """Get response from the OpenAI"""

        response = cls.client.chat.completions.create(
            model="gpt-4o-mini",
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
