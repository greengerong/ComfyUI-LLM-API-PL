from openai import OpenAI
from typing import Dict, List

class LLMRemoteAPIChat:
    """
    API 对话处理器
    """
    def __init__(self):
        self.history = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_config": ("DICT",),
                "system_prompt": ("STRING", {
                    "default": "用户输入绘图提示词扩写系统提示词",
                    "multiline": True
                }),
                "user_prompt": ("STRING", {
                    "default": "请扩写以下提示词：",
                    "multiline": True
                }),
                "enable_history": ("BOOLEAN", {"default": False}),
                "max_history": ("INT", {"default": 10, "min": 5})
            },
            "optional": {
                "history": ("DICT", {"default": None})
            }
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("响应内容", "历史记录")
    CATEGORY = "LLM Remote/处理"
    FUNCTION = "process_chat"

    def process_chat(self, api_config: Dict, system_prompt: str, user_prompt: str,
                    enable_history: bool, max_history: int, history: Dict = None):
        # 初始化客户端
        client = OpenAI(
            api_key=api_config["api_key"],
            base_url=api_config["base_url"]
        )

        # 构建消息
        messages = self._build_messages(system_prompt, user_prompt, history, enable_history, max_history)
        
        try:
            # API调用
            response = client.chat.completions.create(
                model=api_config["model"],
                messages=messages,
                temperature=api_config["temperature"],
                max_tokens=api_config["max_tokens"],
                stream=False
            )
            
            # 更新历史
            new_history = self._update_history(
                messages, response, 
                enable_history, max_history
            )
            return (response.choices[0].message.content, new_history)
        except Exception as e:
            raise RuntimeError(f"API调用失败: {str(e)}")

    def _build_messages(self, system_prompt: str, user_prompt: str, 
                       history: Dict, enable: bool, max_keep: int):
        messages = [{"role": "system", "content": system_prompt}]
        
        if enable and history:
            messages += history.get("messages", [])[-max_keep*2:]
            
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def _update_history(self, messages: List, response, enable: bool, max_keep: int):
        if not enable:
            return {"messages": []}

        new_messages = messages + [{
            "role": "assistant", 
            "content": response.choices[0].message.content
        }]
        
        return {
            "messages": new_messages[-max_keep*2:],  # 保留n轮对话
            "config": {
                "enable_history": enable,
                "max_history": max_keep
            }
        }
