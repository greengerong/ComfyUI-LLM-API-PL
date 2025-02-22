# ComfyUI-Zonos/nodes/manual_config_loader.py
from typing import Dict

class LLMRemoteAPIManualConfig:
    """
    LLM远程API手动配置节点
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("STRING", {"default": "deepseek-chat", "multiline": False}),
                "base_url": ("STRING", {"default": "https://api.deepseek.com", "multiline": False}),
                "api_key": ("STRING", {"default": "your-api-key-here", "multiline": False}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 512}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("api_config",)
    CATEGORY = "LLM Remote/配置"
    FUNCTION = "load_config"

    def load_config(self, model, base_url, api_key, temperature, max_tokens):
        # 参数验证
        if not model:
            raise ValueError("模型名称不能为空")
        if not base_url:
            raise ValueError("Base URL不能为空")
        if not api_key:
            raise ValueError("API Key不能为空")

        # 返回配置字典
        return ({
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },)
