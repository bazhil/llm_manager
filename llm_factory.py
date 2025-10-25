import os
from dotenv import load_dotenv

from managers.deepseek_manager import DeepSeekManager
from managers.giga_chat_manager import GigaChatManager
from managers.ollama_manager import OllamaManager
from managers.open_ai_manager import OpenAIManager
from managers.yandex_gpt_manager import YandexGPTManager


load_dotenv()


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
        provider = os.getenv("PROVIDER", "gigachat")  # Default to "gigachat"
        print(f"LLM_MANAGER - Creating manager for provider: {provider}")

        if provider == "ollama":
            llm_manager = OllamaManager
        elif provider == "deepseek":
            llm_manager = DeepSeekManager
        elif provider == "openai":
            llm_manager = OpenAIManager
        elif provider == "yandex":
            llm_manager = YandexGPTManager
        elif provider == "gigachat":
            llm_manager = GigaChatManager

        else:
            raise ValueError(f"Unsupported provider: {provider}")

        print(f"LLM_MANAGER - Selected manager class: {llm_manager.__name__}")
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
