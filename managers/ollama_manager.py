import os
import logging
from ollama import Client
from ollama import ChatResponse
from dotenv import load_dotenv

from utils import extract_reasoning_text

load_dotenv()
logger = logging.getLogger(__name__)


class OllamaManager:
    """Manage the Ollama"""
    # https://github.com/ollama/ollama-python

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of Ollama client"""
        if cls._client is None:
            host = os.getenv('OLLAMA_HOST')
            logger.info("Initializing Ollama client...")
            logger.info(f"  Host: {host}")
            if not host:
                logger.error("OLLAMA_HOST не установлен")
                raise ValueError("OLLAMA_HOST не установлен в переменных окружения")
            cls._client = Client(host=host)
            logger.info("Ollama client initialized successfully")
        else:
            logger.debug("Using existing client instance")
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str) -> str:
        """Get response from the Ollama"""
        model = os.getenv('OLLAMA_MODEL')
        logger.info("="*60)
        logger.info("GENERATING RESPONSE - Ollama")
        logger.info(f"Model: {model}")
        logger.info(f"Prompt length: {len(prompt)} chars")
        logger.info(f"System prompt length: {len(system_prompt)} chars")

        client = cls._get_client()
        logger.info("Sending request to Ollama API...")
        response: ChatResponse = client.chat(
            model=model,
            messages=[
                {"role": "assistant", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        result = extract_reasoning_text(response['message']['content'])
        logger.info(f"Response received: {len(result)} chars")
        logger.info("="*60)

        return result