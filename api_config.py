import json
import os
import traceback
from typing import Dict

class LLMRemoteAPIConfig:
    """
    API 配置加载器（带缓存和异常处理）
    """
    _config_cache = None  # 配置缓存
    _last_load_error = None  # 最后加载错误信息

    @classmethod
    def INPUT_TYPES(cls):
        # 延迟加载配置
        if cls._config_cache is None and cls._last_load_error is None:
            cls._load_config()

        models = []
        if cls._config_cache:
            models = [m["name"] for m in cls._config_cache.get("models", [])]

        return {
            "required": {
                "config_name": (models, {"default": models[0] if models else ""}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 512}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID_LLMRemoteAPIConfig"
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
            # 检查文件存在性
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"配置文件不存在: {config_path}")

            # 读取文件内容
            with open(config_path, "r", encoding="utf-8") as f:
                raw_data = f.read()
                if not raw_data.strip():
                    raise ValueError("配置文件为空")

            # 解析JSON
            config_data = json.loads(raw_data)
            
            # 验证配置格式
            if "models" not in config_data:
                raise ValueError("配置文件缺少'models'字段")
                
            if not isinstance(config_data["models"], list):
                raise ValueError("'models'字段应为列表类型")

            # 缓存有效配置
            cls._config_cache = config_data
            cls._last_load_error = None

        except Exception as e:
            error_msg = f"配置加载失败: {str(e)}\n{traceback.format_exc()}"
            print(f"[LLMRemote] ERROR: {error_msg}")
            cls._config_cache = None
            cls._last_load_error = error_msg

    def load_config(self, config_name: str, temperature: float, max_tokens: int, unique_id=None):
        # 如果之前加载失败，尝试重新加载一次配置
        if self._last_load_error or not self._config_cache:
            self._load_config()
            
        # 如果重新加载后仍然失败，则抛出异常
        if self._last_load_error:
            raise ValueError(f"配置加载失败，请检查控制台输出\n{self._last_load_error}")

        if not self._config_cache:
            raise ValueError("没有可用的配置，请检查pl-config.json文件")

        model_config = next((m for m in self._config_cache["models"] if m["name"] == config_name), None)
        
        if not model_config:
            available = [m["name"] for m in self._config_cache["models"]]
            raise ValueError(f"未找到配置 '{config_name}'，可用配置: {', '.join(available)}")

        return ({
            "api_key": model_config.get("api_key", ""),
            "base_url": model_config.get("base_url", ""),
            "model": model_config.get("model", ""),
            "temperature": temperature,
            "max_tokens": max_tokens,
        },)