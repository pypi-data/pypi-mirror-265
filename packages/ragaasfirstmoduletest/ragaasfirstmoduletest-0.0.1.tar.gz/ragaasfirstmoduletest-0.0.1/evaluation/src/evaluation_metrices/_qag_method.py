from deepeval.models import GPTModel
import os
from helper_files import llm_model_config
os.environ["HUGGINGFACEHUB_API_TOKEN"] =  llm_model_config.HF.api_token  

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import SummarizationMetric
from typing import Dict, Optional
from LLMPrompts._prompts import QAG_PROMPTS
from helper_files._gpt_chat_completion import GPTCompletion
from pydantic import BaseModel
import json



class InputData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    
    answer : str
    ground_truth : str

class QAGResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines the QAG score based on number of claims correctly captured by the generated answer."
    score: float
    reason: str = None


class QAG_Metric:

    def __init__(self, score_type = None):
        self.score_type = score_type
        pass


    def _parse_prompt(self, type, answer,ground_truth):
        """
        Args: (answer: 'answer' value from input JSON,
              ground_truth: 'ground_truth' value from input JSON)

        Returns: (prompt: Compiled prompt message to give for GPT chat completion)
        """
        if type == 'alignment':
            system_promopt = QAG_PROMPTS['alignment'].get("SYSTEM_PROMPT")
            user_prompt = QAG_PROMPTS['alignment'].get("USER_PROMPT")
            assistant_prompt = QAG_PROMPTS['alignment'].get("ASSISTANT_PROMPT")
            final_prompt = QAG_PROMPTS['alignment'].get("FINAL_PROMPT").format(answer, ground_truth)

            prompt = [
                            {"role": "system", "content": system_promopt},
                            {"role": "user", "content": user_prompt},
                            {"role": "assistant", "content": assistant_prompt},
                            {"role": "user", "content": final_prompt}
                        ]
        elif type == 'coverage':
            system_promopt = QAG_PROMPTS['coverage'].get("SYSTEM_PROMPT")
            user_prompt = QAG_PROMPTS['coverage'].get("USER_PROMPT")
            assistant_prompt = QAG_PROMPTS['coverage'].get("ASSISTANT_PROMPT")
            final_prompt = QAG_PROMPTS['coverage'].get("FINAL_PROMPT").format(answer, ground_truth)
            prompt = [
                            {"role": "system", "content": system_promopt},
                            {"role": "user", "content": user_prompt},
                            {"role": "assistant", "content": assistant_prompt},
                            {"role": "user", "content": final_prompt}
                        ]
                        
        return prompt
        
    def _getscore(self, dataDict):
        """
        Args: (dataDict: input JSON)

        Returns: (resultObj: QAGResult data object having corresponding filled values)
        """
        
        self.dataDict = InputData(**dataDict).dict()
        answer = self.dataDict['answer']
        ground_truth = self.dataDict['ground_truth']
        score_type  = self.score_type

        prompt = self._parse_prompt(score_type, answer,ground_truth)

        gptObj = GPTCompletion(prompt)
        result = gptObj.getResult()
        if isinstance(result, str):
            result = json.loads(result)
        # result = result.replace(": null",': ""')
        # print('result', result)
        # parsed_result = eval(eval(result)['choices'][0]['message']['content'])
        parsed_result = result['choices'][0]['message']['content']
        if isinstance(parsed_result, str):
            parsed_result = json.loads(parsed_result)
        qag_score = parsed_result['QAG_Score']
        reason = parsed_result['Reason']
        

        resultObj = QAGResult(**{"score":qag_score,"reason":reason})

        return resultObj