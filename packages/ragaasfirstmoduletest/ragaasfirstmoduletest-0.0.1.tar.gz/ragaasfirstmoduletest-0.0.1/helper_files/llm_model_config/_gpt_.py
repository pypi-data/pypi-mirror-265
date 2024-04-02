import openai
from . import config

class GPTConfig:
    chat_gpt = config['chat_gpt']
    model_name = chat_gpt['model_name']
    base_url = chat_gpt['base_url']
    api_key = chat_gpt['api_key']
    cert_file = chat_gpt['cert_file']
    engine = chat_gpt["engine"]