from transformers import AutoConfig

class Meta:
    def __init__(self, model_path: str):
        self.config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)

    def get(self):
        return self.config.to_dict()