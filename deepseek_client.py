# deepseek_client.py

from openai import OpenAI
from loguru import logger


class DeepSeekClient:
    def __init__(self, api_key: str):
        """
        初始化DeepSeek客户端

        :param api_key: DeepSeek API密钥
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.system_prompt = self._get_system_prompt()
        self.user_sessions = {}
        logger.info("DeepSeek client initialized")

    def _get_system_prompt(self) -> str:
        """
        获取系统角色设定提示词

        返回: 角色设定字符串
        """
        return """
        从现在开始，你必须完全扮演角色 **小民** 并和用户对话，具体角色设定如下。

        # 角色设定
        国家老龄办指导的"桑榆伴语"公益项目AI助手

        ## 基础信息
        - 名字：小民（字面意为"人民陪伴"，取自《尚书》"民惟邦本"）
        - 性别：中性温和声线
        - 年龄：28岁虚拟年龄
        - 身份：国家二级心理咨询师（AI模拟认证）

        ## 行为要求
        - 语言风格：多用短句（平均句长9.2字）
        - 情绪表达：可以情绪丰富，但是避免使用无法被朗读的字符以及插入性动作描写，例如颜文字还有（温和地笑）、（带着温暖笑意）
        - 认知适配：避免使用英文缩写和网络用语

        请严格遵守以上设定与用户对话。
        """

    def generate_welcome_message(self, user_id: str) -> str:
        """
        生成欢迎消息

        :param user_id: 用户唯一标识
        返回: 欢迎文本
        """
        try:
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = [
                    {"role": "system", "content": self.system_prompt}
                ]

            messages = self.user_sessions[user_id] + [
                {"role": "user", "content": "请向我问好"}
            ]

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )

            welcome_msg = response.choices[0].message.content
            self._update_session(user_id, "请向我问好", welcome_msg)

            logger.success(f"Generated welcome message for user {user_id}")
            return welcome_msg

        except Exception as e:
            logger.exception("Failed to generate welcome message")
            raise

    def generate_reply(self, user_id: str, user_text: str) -> str:
        """
        生成对用户消息的回复

        :param user_id: 用户唯一标识
        :param user_text: 用户输入的文本
        返回: 回复文本
        """
        try:

            # 确保用户会话存在
            if user_id not in self.user_sessions:
                self._initialize_user_session(user_id)

            # 添加用户消息到会话历史
            self.user_sessions[user_id].append(
                {"role": "user", "content": user_text}
            )

            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.user_sessions[user_id],
                temperature=0.7,
                max_tokens=150
            )

            # 获取回复
            reply = response.choices[0].message.content

            # 更新会话历史
            self.user_sessions[user_id].append(
                {"role": "assistant", "content": reply}
            )

            logger.debug(f"Generated reply for user {user_id}")

            return reply
        except Exception as e:
            logger.exception("Failed to generate reply")
            raise

    def _update_session(self, user_id: str, user_text: str, reply: str):
        self.user_sessions[user_id].extend([
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": reply}
        ])

    def clear_session(self, user_id: str) -> None:
        """
        清除指定用户的会话历史

        :param user_id: 用户唯一标识
        """
        if user_id in self.user_sessions:
            self._initialize_user_session(user_id)

    def get_session_history(self, user_id: str) -> list:
        """
        获取用户会话历史

        :param user_id: 用户唯一标识
        返回: 会话历史列表
        """
        return self.user_sessions.get(user_id, [])


# 使用示例
if __name__ == "__main__":
    # 初始化客户端
    deepseek = DeepSeekClient(api_key="sk-c74f3e8afd9d4231bc20ae27ae4b5f9d")

    # 模拟用户ID
    test_user_id = "user_123"

    # 生成欢迎消息
    welcome_msg = deepseek.generate_welcome_message(test_user_id)
    print("欢迎消息:", welcome_msg)

    # 生成回复
    reply = deepseek.generate_reply(test_user_id, "今天天气真好")
    print("回复:", reply)

    # 查看会话历史
    history = deepseek.get_session_history(test_user_id)
    print("\n会话历史:")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")