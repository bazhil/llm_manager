import os
import logging
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
logger = logging.getLogger(__name__)


class OpenAIManager:
    """Manage the OpenAI API"""

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of OpenAI client"""
        if cls._client is None:
            logger.info("Initializing OpenAI client...")
            logger.info(f"  API Key: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
            cls._client = OpenAI()
            logger.info("OpenAI client initialized successfully")
        else:
            logger.debug("Using existing client instance")
        return cls._client

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the OpenAI"""
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        logger.info("="*60)
        logger.info("GENERATING RESPONSE - OpenAI")
        logger.info(f"Model: {model}")
        logger.info(f"Prompt length: {len(prompt)} chars")
        logger.info(f"System prompt length: {len(system_prompt)} chars")

        client = cls._get_client()
        logger.info("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )

        if response:
            answer = response.choices[0].message.content
            logger.info(f"Response received: {len(answer)} chars")
            logger.info("="*60)
            return answer
        else:
            logger.error("No response from OpenAI API")
            return "Error in generating response."
