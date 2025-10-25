import asyncio
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from gigachat.exceptions import ResponseError
from dotenv import load_dotenv


load_dotenv()


class GigaChatManager:
    """Manage the GigaChat API"""

    _client = None
    _client_error = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of GigaChat client with error handling"""
        if cls._client is not None:
            return cls._client
        
        if cls._client_error is not None:
            raise cls._client_error
        
        try:
            auth_key = os.getenv('GIGA_CHAT_AUTH_KEY')
            model = os.getenv('GIGA_CHAT_MODEL')
           
            # Проверка наличия ключа
            if not auth_key or auth_key == 'your-gigachat-auth-key':
                error_msg = (
                    "GIGA_CHAT_AUTH_KEY не установлен или использует placeholder значение!\n"
                    "Для получения ключа:\n"
                    "1. Зарегистрируйтесь на https://developers.sber.ru/portal/products/gigachat\n"
                    "2. Создайте проект и получите credentials (Client Secret)\n"
                    "3. Установите в .env: GIGA_CHAT_AUTH_KEY=ваш-ключ\n"
                    "4. Перезапустите: docker compose restart app"
                )
                cls._client_error = ValueError(error_msg)
                raise cls._client_error
            
            print(f"GIGACHAT - Initializing client with model: {model}")
            cls._client = GigaChat(
                credentials=auth_key,
                verify_ssl_certs=False,
                model=model,
            )
            print("GIGACHAT - Client initialized successfully")
            return cls._client
            
        except ValueError:
            # ValueError уже сохранен в cls._client_error, просто пробрасываем его дальше
            raise
        except ResponseError as e:
            error_msg = (
                f"Ошибка авторизации GigaChat: {str(e)}\n"
                "Возможные причины:\n"
                "1. Неправильный формат GIGA_CHAT_AUTH_KEY (нужен Client Secret из личного кабинета)\n"
                "2. Ключ не активен или истёк\n"
                "3. Проблемы с сетью\n"
                "Проверьте ключ на https://developers.sber.ru/portal/products/gigachat"
            )
            cls._client_error = ValueError(error_msg)
            raise cls._client_error
        except Exception as e:
            error_msg = f"Неожиданная ошибка инициализации GigaChat: {str(e)}"
            cls._client_error = ValueError(error_msg)
            raise cls._client_error

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from GigaChat"""
        try:
            client = cls._get_client()
                        
            response = client.chat(
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
            
            answer = response.choices[0].message.content

            return answer
            
        except ResponseError as e:
            model = os.getenv('GIGA_CHAT_MODEL')
            error_msg = (
                f"Ошибка GigaChat API: {str(e)}\n"
                f"Проверьте:\n"
                f"1. GIGA_CHAT_AUTH_KEY корректен\n"
                f"2. Модель {model} доступна в вашем тарифе\n"
                f"3. Не превышен лимит запросов"
            )
            raise ValueError(error_msg) from e
        except Exception as e:
            raise ValueError(f"Неожиданная ошибка при вызове GigaChat: {str(e)}") from e


if __name__ == '__main__':
    async def main():
        result = await GigaChatManager.get_response("You are a helpful assistant with perfect knowledge of TRIZ theory. Can you work as a TRIZ expert?")

        print(result)


    asyncio.run(main())