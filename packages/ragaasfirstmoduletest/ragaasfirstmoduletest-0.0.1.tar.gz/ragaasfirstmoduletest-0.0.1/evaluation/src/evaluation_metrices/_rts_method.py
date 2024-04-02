import argparse
import json
import os
from tqdm import tqdm
#from prompt_templates import prepare_rts_prompt, prepare_mcq_prompt, prepare_stareval_prompt
from LLMPrompts._prompts import RTS_PROMPTS
from pydantic import BaseModel
import time
# TODO: Important: enable your own openai key
import openai
# from secret import my_key
# TODO- load these from conf/env
openai.api_key = "LLMal16103f15HV!`GLD" #Personalized secured tokenID
openai.api_base = "https://uat-dsmbrsvc.anthem.com/llmgateway/openai"
from helper_files._gpt_chat_completion import GPTCompletion
from typing import Dict, Any,List


class InData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    answer: str
    article: str


# class RTSScore(BaseModel):
#     """
#     Define the dimesion score object values
#     """
#     reason: str = None
#     score: Any

class RTSScore(BaseModel):
    """
    Define the dimesion score object column names
    """
    name: str
    score: Dict

class ReasonThenScoreResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines different dimensions like coherence, consistency, fluency and relevance of the generated summary compared to the given article"
    score: List







class ReasonThenScore:

    def __init__(self,dataDict):
        self.dataDict = InData(**dataDict).dict()

    
    def _get_gpt_response(self,prompt):
        prompt_message = [{'role':'system','content':prompt}]
        gptObj = GPTCompletion(prompt_message)
        response = gptObj.getResult()
        response = response.replace(": null",': ""')
        parsed_response = eval(response)["choices"][0]["message"]["content"]
        return eval(parsed_response)

    def _relevance(self):
        summary = self.dataDict['answer']
        article = self.dataDict['article']
        prompt = RTS_PROMPTS.get('PROMPT_FOR_RELEVANCE').replace('{article}',article).replace('{summary}',summary)
        resp = self._get_gpt_response(prompt)
        return resp
    def _consistency(self):
        summary = self.dataDict['answer']
        article = self.dataDict['article']
        prompt = RTS_PROMPTS.get('PROMPT_FOR_CONSISTENCY').replace('{article}',article).replace('{summary}',summary)
        resp = self._get_gpt_response(prompt)
        return resp
    def _fluency(self):
        summary = self.dataDict['answer']
        article = self.dataDict['article']
        prompt = RTS_PROMPTS.get('PROMPT_FOR_FLUENCY').replace('{article}',article).replace('{summary}',summary)
        resp = self._get_gpt_response(prompt)
        return resp
    def _coherence(self):
        summary = self.dataDict['answer']
        article = self.dataDict['article']
        prompt = RTS_PROMPTS.get('PROMPT_FOR_COHERENCE').replace('{article}',article).replace('{summary}',summary)
        resp = self._get_gpt_response(prompt)
        return resp

    def _getscore(self):
        relevance_result = self._relevance()
        fluency_result = self._fluency()
        coherence_result = self._coherence()
        consistency_result = self._consistency()
        result = ReasonThenScoreResult(**{"score":[RTSScore(**{"name":"relevance","score":relevance_result}),RTSScore(**{"name":"fluency","score":fluency_result}),
                  RTSScore(**{"name":"coherence","score":coherence_result}),RTSScore(**{"name":"consistency","score":consistency_result})]})
        return result

