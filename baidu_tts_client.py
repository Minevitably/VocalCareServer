from aip import AipSpeech
from loguru import logger


class BaiduTTSClient:
    def __init__(self, app_id: str, api_key: str, secret_key: str):
        self.client = AipSpeech(app_id, api_key, secret_key)
        logger.info("Baidu TTS client initialized")

    def text_to_speech(self, text: str, lang: str = 'zh', ctp: int = 1, options: dict = None) -> bytes:
        default_options = {
            'vol': 5, 'per': 0, 'spd': 6, 'pit': 5
        }

        if options:
            default_options.update(options)

        try:
            logger.debug(f"Converting text to speech (first 50 chars): {text[:50]}...")
            result = self.client.synthesis(text, lang, ctp, default_options)

            if isinstance(result, dict):
                error_msg = result.get('err_msg', 'unknown error')
                logger.error(f"TTS failed: {error_msg}")
                raise RuntimeError(f"TTS error: {error_msg}")

            logger.success("Text converted to speech successfully")
            return result

        except Exception as e:
            logger.exception("TTS conversion failed")
            raise