
from deepeval.models import GPTModel
import openai
from openai import OpenAI
from pathlib import Path
file_path = Path(__file__).resolve().parent
import os


from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import SummarizationMetric
from typing import Dict, Optional
from pydantic import BaseModel
from helper_files import llm_model_config

os.environ["HUGGINGFACEHUB_API_TOKEN"] = llm_model_config.HF.api_token 


class InputData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    answer : str
    ground_truth : str

class AlignmentCoverageResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines the alignment and coverage of summary corresponding to the given article"
    score: dict
    reason: str = None


class GPTModel_OpenAI(GPTModel):
    def __init__(
        self,
        model: Optional[str] = None,
        *args,
        **kwargs,
    ):
        model_name = model
        self.model_name = model

        super().__init__(model_name, *args, **kwargs)
    def load_model(self):
        return OpenAI(base_url=llm_model_config.GPT.base_url, api_key= llm_model_config.GPT.api_key).chat.completions.create
    def invoke(self,model,prompt):
        response = model(model = llm_model_config.GPT.model_name,   
                        messages = [{"role":"system","content":prompt}], 
                        frequency_penalty = 0, 
                        temperature=0,  
                        presence_penalty = 0)
        result = response.replace(": null",': ""')
        parsed_result = eval(result)['choices'][0]['message']['content']
        return parsed_result
    # @retry_with_exponential_backoff
    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return self.invoke(chat_model,prompt)



class AlignmentCoverageScore:
    
    def __init__(self):
        pass
        
    def _getscore(self,dataDict):
        """
        Args: (dataDict: input JSON)

        Returns: (resultObj: AlignmentCoverageResult data object having corresponding filled values)
        """
        self.dataDict = InputData(**dataDict).dict()
        answer = self.dataDict['answer']
        ground_truth = self.dataDict['ground_truth']

        test_case = LLMTestCase(
          input=ground_truth, 
          actual_output=answer
        )

        de_model = GPTModel_OpenAI(model = llm_model_config.GPT.model_name)
        summarization_metric = SummarizationMetric(
            model = de_model
        )

        result = evaluate([test_case], [summarization_metric])

        scores = result[0].metrics[0].score_breakdown
        reason = result[0].metrics[0].reason
        resultObj = AlignmentCoverageResult(**{"score":scores,"reason":reason})

        return resultObj

