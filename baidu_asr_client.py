from aip import AipSpeech
from loguru import logger
from typing import Union


class BaiduASRClient:
    def __init__(self, app_id: str, api_key: str, secret_key: str):
        """
        初始化百度语音识别(ASR)客户端 - 专用于PCM格式

        :param app_id: 百度APP ID
        :param api_key: 百度API Key
        :param secret_key: 百度Secret Key
        """
        self.client = AipSpeech(app_id, api_key, secret_key)
        logger.info("Baidu ASR client initialized (PCM only)")

    def speech_to_text(self, audio_data: Union[bytes, str],
                       rate: int = 16000,
                       dev_pid: int = 1537) -> str:
        """
        将PCM格式语音转换为文本

        :param audio_data: 音频二进制数据或文件路径
        :param rate: 采样率(默认16000)
        :param dev_pid: 语言模型(1537-普通话)
        返回: 识别出的文本
        """
        try:
            # 如果是文件路径，读取文件内容
            if isinstance(audio_data, str):
                logger.debug(f"Reading PCM file: {audio_data}")
                with open(audio_data, 'rb') as f:
                    audio_data = f.read()

            if not isinstance(audio_data, bytes):
                raise ValueError("Audio data must be bytes or file path")

            logger.debug(f"Converting PCM audio to text (size: {len(audio_data)} bytes)")

            # 调用百度ASR API
            result = self.client.asr(
                audio_data,
                'pcm',
                rate,
                {'dev_pid': dev_pid}
            )

            # 检查识别结果
            if result.get('err_no') != 0:
                error_msg = result.get('err_msg', 'unknown error')
                logger.error(f"ASR failed (err_no: {result.get('err_no')}): {error_msg}")
                raise RuntimeError(f"ASR error: {error_msg}")

            text = result.get('result', [''])[0]
            logger.success(f"ASR result: {text}")
            return text

        except Exception as e:
            logger.exception("PCM audio recognition failed")
            raise

    def recognize_pcm_file(self, file_path: str, **kwargs) -> str:
        """
        识别PCM音频文件(便捷方法)

        :param file_path: PCM文件路径
        :param kwargs: 其他参数(rate, dev_pid等)
        返回: 识别出的文本
        """
        return self.speech_to_text(file_path, **kwargs)


def create_baidu_asr_client(config: dict) -> BaiduASRClient:
    """
    创建百度语音识别(ASR)客户端

    :param config: 包含app_id, api_key, secret_key的字典
    返回: BaiduASRClient实例
    """
    try:
        required_keys = {'app_id', 'api_key', 'secret_key'}
        if not all(key in config for key in required_keys):
            raise ValueError("Missing required Baidu ASR configuration keys")

        return BaiduASRClient(**{k: config[k] for k in required_keys})

    except Exception as e:
        logger.error(f"Failed to initialize Baidu ASR client: {e}")
        raise


if __name__ == "__main__":
    # 测试代码
    from config import BAIDU_ASR_CONFIG
    from loguru import logger

    logger.add("asr_test.log", rotation="1 MB", level="DEBUG")

    try:
        # 初始化客户端
        asr_client = create_baidu_asr_client(BAIDU_ASR_CONFIG)

        # 测试1: 直接使用PCM文件路径
        test_file = "audio.pcm"  # 替换为你的PCM文件路径
        logger.info(f"Testing with PCM file: {test_file}")

        text = asr_client.recognize_pcm_file(test_file)
        print(f"识别结果: {text}")

        # 测试2: 使用二进制数据
        logger.info("Testing with PCM bytes data")
        with open(test_file, 'rb') as f:
            pcm_data = f.read()

        text = asr_client.speech_to_text(pcm_data)
        print(f"识别结果: {text}")

    except Exception as e:
        logger.error(f"ASR test failed: {e}")