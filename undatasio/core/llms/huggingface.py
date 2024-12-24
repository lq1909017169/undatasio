from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from pydantic import BaseModel


class HuggingFaceLLM(BaseModel):
    repo_id: str
    task: str
    max_new_tokens: int
    do_sample: bool
    repetition_penalty: float
    endpoint_url: str
    max_new_tokens: int
    top_k: int
    top_p: float
    typical_p: float
    temperature: float
    huggingfacehub_api_token: str

    def langchain(self):
        pass

    def llama_index(self):
        pass
