import os
import logging
from dotenv import load_dotenv

from managers.deepseek_manager import DeepSeekManager
from managers.giga_chat_manager import GigaChatManager
from managers.ollama_manager import OllamaManager
from managers.open_ai_manager import OpenAIManager
from managers.yandex_gpt_manager import YandexGPTManager


load_dotenv()
logger = logging.getLogger(__name__)


class LLMFactory:
    """
    A factory class to create and return the appropriate LLM manager based on the environment configuration.
    By default, it returns an Ollama manager connected to a local Ollama instance.
    """

    def __init__(self):
        self.llm_manager = self._create_llm_manager()

    def _create_llm_manager(self):
        """
        Create and return the LLM manager based on the key defined in the .env file.

        Returns:
            LLMManager: An instance of the appropriate LLM manager.
        """
        provider = os.getenv("PROVIDER", "ollama")
        logger.info("="*60)
        logger.info("INITIALIZING LLM")
        logger.info(f"Provider from env: {provider}")

        if provider == "ollama":
            llm_manager = OllamaManager
            logger.info("Selected: Ollama")
            logger.info(f"  Host: {os.getenv('OLLAMA_HOST', 'NOT SET')}")
            logger.info(f"  Model: {os.getenv('OLLAMA_MODEL', 'NOT SET')}")
        elif provider == "deepseek":
            llm_manager = DeepSeekManager
            logger.info("Selected: DeepSeek")
            logger.info(f"  API Key: {'SET' if os.getenv('DEEPSEEK_API_KEY') else 'NOT SET'}")
        elif provider == "openai":
            llm_manager = OpenAIManager
            logger.info("Selected: OpenAI")
            logger.info(f"  API Key: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
            logger.info(f"  Model: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")
        elif provider == "yandex":
            llm_manager = YandexGPTManager
            logger.info("Selected: Yandex GPT")
            logger.info(f"  API Key: {'SET' if os.getenv('YANDEX_GPT_API_KEY') else 'NOT SET'}")
        elif provider == "gigachat":
            llm_manager = GigaChatManager
            logger.info("Selected: GigaChat")
            logger.info(f"  Auth Key: {'SET' if os.getenv('GIGA_CHAT_AUTH_KEY') else 'NOT SET'}")
            logger.info(f"  Model: {os.getenv('GIGA_CHAT_MODEL', 'GigaChat')}")
        else:
            logger.error(f"Unsupported provider: {provider}")
            raise ValueError(f"Unsupported provider: {provider}")

        logger.info(f"Manager class ready: {llm_manager.__name__}")
        logger.info("="*60)
        return llm_manager


    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from the LLM"""

        return await cls().llm_manager.get_response(system_prompt, prompt)


def get_llm_manager():
    """
    Factory function to get LLM manager instance.
    Returns the appropriate manager class based on the PROVIDER environment variable.
    """
    factory = LLMFactory()
    return factory.llm_manager
