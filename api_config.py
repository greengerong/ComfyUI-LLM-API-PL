import json
import os
from typing import Dict

class LLMRemoteAPIConfig:
    """
    API 配置加载器
    """
    @classmethod
    def INPUT_TYPES(cls):
        config = cls._load_config()
        models = [m["name"] for m in config["models"]] if config else []

        return {
            "required": {
                "config_name": (models, {"default": models[0] if models else ""}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 512}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("api_config",)
    CATEGORY = "LLM Remote/配置"
    FUNCTION = "load_config"

    @classmethod
    def _load_config(cls):
        config_path = os.path.join(os.path.dirname(__file__), "pl-config.json")
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"配置加载失败: {str(e)}")
            return {"models": []}

    def load_config(self, config_name: str, temperature: float, max_tokens: int):
        config_data = self._load_config()
        model_config = next((m for m in config_data["models"] if m["name"] == config_name), None)
        
        if not model_config:
            raise ValueError(f"未找到配置: {config_name}")

        return {
            "api_key": model_config["api_key"],
            "base_url": model_config["base_url"],
            "model": model_config["model"],
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
