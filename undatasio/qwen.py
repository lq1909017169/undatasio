from typing import List, Dict
from qwen_agent.memory import Memory
from .undatasio import UnDatasIO
from qwen_agent.agents import Assistant
from .untils import LLMConfig
import re
import json


class QwenAgentRag:

    def __init__(self, undatasio: UnDatasIO, llm_config: LLMConfig):
        self.undatasio = undatasio
        self.llm_config = {
            '': {
                'api_key': llm_config.api_key,
                'model': llm_config.model,
                'model_server': llm_config.model_server
            }
        }

    def _files(self, file_name_list, version):
        return self.undatasio.get_result_to_files(
            file_name_list=file_name_list,
            version=version,
        )['data']

    def _local_db(self):
        bot = Assistant(llm=self.llm_config)


        messages = [{'role': 'user', 'content': [{'text': prompt}, {'file': }]}]
        rsp = bot.run_nonstream(messages)[0]['content']
        json_pattern = re.compile(r'\{(.*?)\}', re.DOTALL)
        match = re.search(json_pattern, rsp)
        json_str = match.group(0)
        json_data = json.loads(json_str)


def get_values(keys: List, file: str) -> Dict | None:
    keys_list = [f"{k}: 提取关于{k}的答案，没有则为空字符串" for k in keys]
    prompt = f"""根据文件中的内容完成任务，输出json格式数据：

    任务：{keys_list}
    """
    bot = Assistant(llm=LLM_CONFIG)
    messages = [{'role': 'user', 'content': [{'text': prompt}, {'file': f'{file}'}]}]
    rsp = bot.run_nonstream(messages)[0]['content']
    json_pattern = re.compile(r'\{(.*?)\}', re.DOTALL)
    match = re.search(json_pattern, rsp)
    json_str = match.group(0)
    json_data = json.loads(json_str)
    return json_data
