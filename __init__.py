from .api_config import LLMRemoteAPIConfig
from .api_chat import LLMRemoteAPIChat
from .LLMThinkParser import LLMThinkParser


NODE_CLASS_MAPPINGS = {
    "LLMRemoteAPIConfig": LLMRemoteAPIConfig,
    "LLMRemoteAPIChat": LLMRemoteAPIChat,
     "LLMThinkParser": LLMThinkParser
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMRemoteAPIConfig": "🌐 API 配置加载",
    "LLMRemoteAPIChat": "💬 API 对话处理",
    "LLMThinkParser": "📖 Think标签解析器"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
