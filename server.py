from deepseek_client import DeepSeekClient
from baidu_tts_client import BaiduTTSClient
from baidu_asr_client import BaiduASRClient
from config import DEEPSEEK_API_KEY, BAIDU_TTS_CONFIG, BAIDU_ASR_CONFIG
from loguru import logger


class ServerAPI:
    def __init__(self):
        """初始化服务器，创建所有必要的服务客户端"""
        try:
            logger.info("Initializing server components...")

            # 初始化所有服务客户端
            self.deepseek_client = DeepSeekClient(api_key=DEEPSEEK_API_KEY)
            self.baidu_tts_client = BaiduTTSClient(**BAIDU_TTS_CONFIG)
            self.baidu_asr_client = BaiduASRClient(**BAIDU_ASR_CONFIG)  # 使用更新后的ASR客户端

            logger.success("Server initialized successfully")

        except Exception as e:
            logger.critical(f"Server initialization failed: {e}")
            raise

    def handle_new_client_connection(self, user_id: str) -> bytes:
        """
        处理新客户端连接
        :param user_id: 用户唯一标识
        :return: 欢迎音频二进制数据
        """
        try:
            logger.info(f"Handling new connection for user {user_id}")

            # 1. 生成欢迎文本
            welcome_text = self.deepseek_client.generate_welcome_message(user_id)

            # 2. 转换为语音
            welcome_audio = self.baidu_tts_client.text_to_speech(welcome_text)

            # 3. 存储会话状态 (伪代码)
            # self.user_sessions_db.create_session(user_id, welcome_text)

            logger.success(f"Generated welcome audio for user {user_id}")
            return welcome_audio

        except Exception as e:
            logger.error(f"Failed to handle new connection: {e}")
            raise

    def handle_user_audio(self, user_id: str, audio_data: bytes) -> bytes:
        """
        处理用户音频消息
        :param user_id: 用户唯一标识
        :param audio_data: 音频二进制数据
        :return: 回复音频二进制数据
        """
        try:
            logger.info(f"Processing audio message from user {user_id}")

            # 1. 语音转文本
            user_text = self.baidu_asr_client.speech_to_text(audio_data)
            logger.debug(f"Recognized text: {user_text}")

            # 2. 获取会话历史 (伪代码)
            # history = self.user_sessions_db.get_session_history(user_id)

            # 3. 生成回复
            reply_text = self.deepseek_client.generate_reply(user_id, user_text)

            # 4. 文本转语音
            reply_audio = self.baidu_tts_client.text_to_speech(reply_text)

            # 5. 更新会话历史 (伪代码)
            # self.user_sessions_db.update_session(user_id, user_text, reply_text)

            logger.success(f"Generated reply audio for user {user_id}")
            return reply_audio

        except Exception as e:
            logger.error(f"Failed to process user audio: {e}")
            raise


if __name__ == "__main__":
    # 测试服务器功能
    try:
        server = ServerAPI()

        # 测试新用户连接
        test_user = "test_user_001"
        welcome_audio = server.handle_new_client_connection(test_user)
        with open('welcome.wav', 'wb') as f:
            f.write(welcome_audio)
            logger.info("Saved welcome audio to welcome.wav")

        # 测试处理用户音频(使用真实音频文件测试)
        with open('audio.pcm', 'rb') as f:
            test_audio = f.read()

        reply_audio = server.handle_user_audio(test_user, test_audio)
        with open('reply.wav', 'wb') as f:
            f.write(reply_audio)
            logger.info("Saved reply audio to reply.wav")

    except Exception as e:
        logger.error(f"Server test failed: {e}")