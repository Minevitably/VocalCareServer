from openai import OpenAI


class DeepSeekChat:
    def __init__(self, api_key, system_prompt="You are a helpful assistant"):
        """
        初始化DeepSeek对话客户端

        :param api_key: 你的DeepSeek API密钥
        :param system_prompt: 系统提示词，用于设定助手行为
        """
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, user_input, stream=False, temperature=0.7, max_tokens=None):
        """
        与DeepSeek模型进行对话

        :param user_input: 用户输入内容
        :param stream: 是否使用流式响应
        :param temperature: 控制回复随机性(0-1)
        :param max_tokens: 回复的最大token数
        :return: 模型回复内容
        """
        # 添加用户消息到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})

        # 准备API请求参数
        params = {
            "model": "deepseek-chat",
            "messages": self.conversation_history,
            "temperature": temperature,
            "stream": stream
        }

        if max_tokens:
            params["max_tokens"] = max_tokens

        # 发送请求
        response = self.client.chat.completions.create(**params)

        # 获取回复内容
        if stream:
            # 处理流式响应
            full_response = []
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response.append(content)
                    print(content, end="", flush=True)
            assistant_reply = "".join(full_response)
        else:
            # 处理普通响应
            assistant_reply = response.choices[0].message.content
            print(assistant_reply)

        # 将助手回复添加到对话历史
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def clear_history(self):
        """清空对话历史(保留系统提示)"""
        self.conversation_history = [self.conversation_history[0]]

    def get_history(self):
        """获取完整的对话历史"""
        return self.conversation_history

    def set_system_prompt(self, new_prompt):
        """更新系统提示词"""
        self.conversation_history[0]["content"] = new_prompt


# 使用示例
if __name__ == "__main__":
    # 替换为你的API密钥
    API_KEY = "sk-c74f3e8afd9d4231bc20ae27ae4b5f9d"

    # 初始化对话
    chat = DeepSeekChat(api_key=API_KEY, system_prompt="你是一个专业的AI助手")

    # 第一轮对话
    print("用户: 你好")
    chat.chat("你好")

    # 第二轮对话(会记住上下文)
    print("\n用户: 我刚才说了什么?")
    chat.chat("我刚才说了什么?")

    # 查看完整对话历史
    print("\n当前对话历史:")
    for msg in chat.get_history():
        print(f"{msg['role']}: {msg['content']}")

    # 清空历史(测试)
    chat.clear_history()
    print("\n清空后对话历史:", chat.get_history())