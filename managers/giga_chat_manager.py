import asyncio
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv


load_dotenv()


class GigaChatManager:
    """Manage the GigaChat API"""

    client = GigaChat(
        credentials=os.getenv('GIGA_CHAT_AUTH_KEY'),
        verify_ssl_certs=False,
        model=os.getenv('GIGA_CHAT_MODEL'),
    )

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from GigaChat"""

        response = cls.client.chat(
            Chat(
                messages=[
                    Messages(
                        role=MessagesRole.SYSTEM,
                        content=system_prompt
                    ),
                    Messages(
                        role=MessagesRole.USER,
                        content=prompt
                    )
                ],
                temperature=0.7,
                max_tokens=1024
            )
        )

        return response.choices[0].message.content


if __name__ == '__main__':
    async def main():
        result = await GigaChatManager.get_response("You are a helpful assistant with perfect knowledge of TRIZ theory. Can you work as a TRIZ expert?")

        print(result)


    asyncio.run(main())