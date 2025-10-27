import asyncio
import os
import logging
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from gigachat.exceptions import ResponseError
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


class GigaChatManager:
    """Manage the GigaChat API"""

    _client = None
    _client_error = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of GigaChat client with error handling"""
        if cls._client is not None:
            logger.debug("Using existing client instance")
            return cls._client
        
        if cls._client_error is not None:
            logger.error("Previous initialization failed")
            raise cls._client_error
        
        try:
            auth_key = os.getenv('GIGA_CHAT_AUTH_KEY')
            model = os.getenv('GIGA_CHAT_MODEL', 'GigaChat-2')
            
            logger.info("Initializing GigaChat client...")
            logger.info(f"  Model: {model}")
            logger.info(f"  Auth Key: {'SET' if auth_key else 'NOT SET'}")
           
            if not auth_key or auth_key == 'your-gigachat-auth-key':
                error_msg = (
                    "GIGA_CHAT_AUTH_KEY не установлен или использует placeholder значение!\n"
                    "Для получения ключа:\n"
                    "1. Зарегистрируйтесь на https://developers.sber.ru/portal/products/gigachat\n"
                    "2. Создайте проект и получите credentials (Client Secret)\n"
                    "3. Установите в .env: GIGA_CHAT_AUTH_KEY=ваш-ключ\n"
                    "4. Перезапустите: docker compose restart app"
                )
                logger.error(error_msg)
                cls._client_error = ValueError(error_msg)
                raise cls._client_error
            
            cls._client = GigaChat(
                credentials=auth_key,
                verify_ssl_certs=False,
                model=model,
            )
            logger.info("GigaChat client initialized successfully")
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
        logger.info("="*60)
        logger.info("GENERATING RESPONSE - GigaChat")
        logger.info(f"Model: {os.getenv('GIGA_CHAT_MODEL', 'GigaChat')}")
        logger.info(f"Prompt length: {len(prompt)} chars")
        logger.info(f"System prompt length: {len(system_prompt)} chars")
        
        try:
            client = cls._get_client()
            
            logger.info("Sending request to GigaChat API...")
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
            logger.info(f"Response received: {len(answer)} chars")
            logger.info("="*60)

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