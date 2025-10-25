import os

from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML


load_dotenv()


class YandexGPTManager:
    """Manage the YandexGPT API"""

    _sdk = None

    @classmethod
    def _get_sdk(cls):
        """Lazy initialization of YandexGPT SDK"""
        if cls._sdk is None:
            folder_id = os.getenv("YANDEX_GPT_FOLDER_ID")
            api_key = os.getenv("YANDEX_GPT_API_KEY")
            if not folder_id or not api_key:
                raise ValueError("YANDEX_GPT_FOLDER_ID и YANDEX_GPT_API_KEY должны быть установлены")
            cls._sdk = YCloudML(folder_id=folder_id, auth=api_key)
        return cls._sdk

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the YandexGPT"""

        sdk = cls._get_sdk()
        response = sdk.models.completions("yandexgpt").configure(temperature=0.5).run(
            messages=[
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": prompt}
            ]
        )

        result = ""
        for alternative in response:
            result += alternative.text

        return result
