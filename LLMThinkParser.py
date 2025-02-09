import re

class LLMThinkParser:
    """
    动态标签解析器
    根据输入标签解析结构化内容
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "default": """<think>
好的，我现在需要帮用户生成一段详细的画面描述提示词...
</think>
A young Chinese woman dressed in...""",
                    "multiline": True
                }),
                "tag_name": ("STRING", {"default": "think"}),  # 新增标签名称参数
                "strict_mode": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("think_content", "generated_prompt")
    CATEGORY = "LLM Processing"
    FUNCTION = "parse_llm_output"

    def parse_llm_output(self, input_text, tag_name, strict_mode):
        # 转义标签名称防止正则注入
        safe_tag = re.escape(tag_name.strip())
        pattern = fr'<{safe_tag}>\n?(.*?)\n?</{safe_tag}>\n*\s*(.*)'
        
        # 预处理：统一换行符并移除首尾空白
        normalized_text = input_text.replace('\r\n', '\n').strip()
        
        # 动态生成正则表达式
        match = re.search(pattern, normalized_text, re.DOTALL | re.IGNORECASE)
        
        think_content = ""
        generated_prompt = ""

        if match:
            think_content = match.group(1).strip()
            prompt_part = match.group(2).strip()
            # 二次清理可能的残留标签
            generated_prompt = re.sub(fr'</?{safe_tag}>', '', prompt_part, flags=re.IGNORECASE)
        elif not strict_mode:
            # 容错处理逻辑
            parts = re.split(r'\n{2,}', normalized_text, 1)
            think_content = parts[0].strip() if len(parts) > 0 else ""
            generated_prompt = parts[1].strip() if len(parts) > 1 else normalized_text

        # 后处理优化
        think_content = re.sub(r'\s{3,}', '  ', think_content)  # 压缩多余空格
        generated_prompt = re.sub(r'\n{2,}', '\n', generated_prompt)  # 保留单换行
        
        return (think_content, generated_prompt)