import os
import logging

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
logger = logging.getLogger(__name__)


class DeepSeekManager:
    """Manage the Deepseek API"""

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of DeepSeek client"""
        if cls._client is None:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            logger.info("Initializing DeepSeek client...")
            logger.info(f"  API Key: {'SET' if api_key else 'NOT SET'}")
            logger.info(f"  Base URL: https://api.deepseek.com")
            if not api_key:
                logger.error("DEEPSEEK_API_KEY не установлен")
                raise ValueError("DEEPSEEK_API_KEY не установлен в переменных окружения")
            cls._client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            logger.info("DeepSeek client initialized successfully")
        else:
            logger.debug("Using existing client instance")
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the Deepseek"""
        logger.info("="*60)
        logger.info("GENERATING RESPONSE - DeepSeek")
        logger.info("Model: deepseek-chat")
        logger.info(f"Prompt length: {len(prompt)} chars")
        logger.info(f"System prompt length: {len(system_prompt)} chars")

        client = cls._get_client()
        logger.info("Sending request to DeepSeek API...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        if response:
            answer = response.choices[0].message.content
            logger.info(f"Response received: {len(answer)} chars")
            logger.info("="*60)
            return answer
        else:
            logger.error("No response from DeepSeek API")
            return "Error in generating response."
