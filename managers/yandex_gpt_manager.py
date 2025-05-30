import os

from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML


load_dotenv()


class YandexGPTManager:
    """Manage the YandexGPT API"""

    sdk = YCloudML(
        folder_id=os.getenv("YANDEX_GPT_FOLDER_ID"),
        auth=os.getenv("YANDEX_GPT_API_KEY"),
    )

    @classmethod
    async def get_response(cls, system_prompt: str, prompt: str):
        """Get response from the YandexGPT"""

        response = cls.sdk.models.completions("yandexgpt").configure(temperature=0.5).run(
            messages=[
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": prompt}
            ]
        )

        result = ""
        for alternative in response:
            result += alternative.text

        return result
