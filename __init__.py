from .api_config import LLMRemoteAPIConfig
from .api_chat import LLMRemoteAPIChat
from .LLMThinkParser import LLMThinkParser
from .manual_config_loader import LLMRemoteAPIManualConfig


NODE_CLASS_MAPPINGS = {
    "LLMRemoteAPIConfig": LLMRemoteAPIConfig,
    "LLMRemoteAPIManualConfig": LLMRemoteAPIManualConfig,
    "LLMRemoteAPIChat": LLMRemoteAPIChat,
    "LLMThinkParser": LLMThinkParser
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMRemoteAPIConfig": "🌐 LLM远程API配置文件加载",
    "LLMRemoteAPIManualConfig": "🌐 LLM远程API手动配置",
    "LLMRemoteAPIChat": "💬 API 对话处理",
    "LLMThinkParser": "📖 Think标签解析器"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
