import openai
from tenacity import retry
# TODO, pick this from env/conf

import os
#os.environ['CURL_CA_BUNDLE'] = ""
from pydantic import BaseModel
from typing import List
from typing import Union
from openai import OpenAI


from helper_files import llm_model_config
from .helper_gpt_gateway import robust_call_openai_gateway

class PromptMessage(BaseModel):
    role : str
    content : str

class PromptMessages(BaseModel):
    pmt : List[PromptMessage]


class GPTCompletion:

    def __init__(self,messages):
        # os.environ["SSL_CERT_FILE"] = llm_model_config.GPT.cert_file 
        # os.environ["REQUESTS_CA_BUNDLE"]= llm_model_config.GPT.cert_file 
        self.messages = PromptMessages(**{"pmt":messages}).dict()['pmt']
        # get the api url/ key from env/conf 
        self.model = OpenAI(base_url=llm_model_config.GPT.base_url,
                             api_key= llm_model_config.GPT.api_key).chat.completions.create
        # self.model = robust_call_openai_gateway
        # self.engine = llm_model_config.GPT.engine
    

    # @retry
    def getResult(self):
        response = self.model(model = llm_model_config.GPT.model_name,   
                        messages =self.messages,
                        frequency_penalty = 0,
                        temperature=0,  
                        presence_penalty = 0)
        return response

        # response = self.model(model = llm_model_config.GPT.model_name,
        #                       prompt = self.messages,
        #                       token_id = llm_model_config.GPT.api_key,
        #                         frequency_penalty = 0, 
        #                         temperature=0,
        #                         sys_prompt = None,
        #                         engine = "gpt3",
        #                         presence_penalty = 0)
        # return response