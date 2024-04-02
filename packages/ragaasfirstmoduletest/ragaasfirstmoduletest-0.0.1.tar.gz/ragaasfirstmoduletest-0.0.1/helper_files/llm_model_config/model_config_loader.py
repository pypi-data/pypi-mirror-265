import yaml

# with open(conf_path, 'r') as f:
#     config = yaml.safe_load(f)

class LLMModelConfig:

    def __init__(self,filepath):
        with open(filepath, 'r') as f:
            self.config = yaml.safe_load(f)

class GPTConfig(LLMModelConfig):
        chat_gpt = self.config['chat_gpt']
        model_name = chat_gpt['model_name']
        base_url = chat_gpt['base_url']
        api_key = chat_gpt['api_key']
        cert_file = chat_gpt['cert_file']