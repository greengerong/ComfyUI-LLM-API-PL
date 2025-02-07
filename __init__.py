from .api_config import LLMRemoteAPIConfig
from .api_chat import LLMRemoteAPIChat

NODE_CLASS_MAPPINGS = {
    "LLMRemoteAPIConfig": LLMRemoteAPIConfig,
    "LLMRemoteAPIChat": LLMRemoteAPIChat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMRemoteAPIConfig": "🌐 API 配置加载",
    "LLMRemoteAPIChat": "💬 API 对话处理"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
