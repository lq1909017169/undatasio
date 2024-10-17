class LLMConfig:

    def __init__(
            self, model: str, model_server: str, api_key: str
    ):
        self.model = model
        self.model_server = model_server
        self.api_key = api_key

