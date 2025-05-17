from openai import OpenAI
from loguru import logger


class DeepSeekClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.system_prompt = self._get_system_prompt()
        self.user_sessions = {}
        logger.info("DeepSeek client initialized")

    def _get_system_prompt(self) -> str:
        return """(角色设定同之前保持不变)"""

    def generate_welcome_message(self, user_id: str) -> str:
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
        try:
            if user_id not in self.user_sessions:
                self.generate_welcome_message(user_id)

            self.user_sessions[user_id].append(
                {"role": "user", "content": user_text}
            )

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.user_sessions[user_id],
                temperature=0.7,
                max_tokens=150
            )

            reply = response.choices[0].message.content
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