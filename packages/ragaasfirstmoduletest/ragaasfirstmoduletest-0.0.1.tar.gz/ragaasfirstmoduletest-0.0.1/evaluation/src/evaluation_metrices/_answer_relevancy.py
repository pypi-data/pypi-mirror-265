# from . import LLMTestCase
# import SummarizationTask.evalSumm as evalsum
from deepeval.models import GPTModel
import openai
import os
import json
from helper_files import llm_model_config



from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from typing import Dict, Optional
from pydantic import BaseModel
from openai import OpenAI

class InputData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    question : str
    answer : str

class AnswerRelevancyResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines the alignment and coverage of summary corresponding to the given article"
    score: float
    reason: str = None


class GPTModel_OpenAI(GPTModel):
    def __init__(
                    self,
                    model: Optional[str] = None,
                    *args,
                    **kwargs,
                ):
        """
        Args: (model: GPT model name)        
        """
        model_name = model
        self.model_name = model

        super().__init__(model_name, *args, **kwargs)
    
    def load_model(self):
        """
        Returns: GPT chat completion method
        """
        # TODO- get the variables from conf/ env
        os.environ["SSL_CERT_FILE"] = llm_model_config.GPT.cert_file#os.path.join(os.getcwd(), 'RAGAAS', "evaluation", 'src', 'evaluation_metrices', "root.pem")
        os.environ["REQUESTS_CA_BUNDLE"]= llm_model_config.GPT.cert_file #os.path.join(os.getcwd(), 'RAGAAS', "evaluation", 'src', 'evaluation_metrices', "root.pem")
        return OpenAI(base_url=llm_model_config.GPT.base_url, api_key= llm_model_config.GPT.api_key).chat.completions.create
    
    def invoke(self,model,prompt):
        """
        Args: (model: GPT chat completion method,
              prompt: The prompt for calculation of the answer relevance score)

        Returns: (parsed_result: Parsed content from GPT chat completion response)
        """
        response = model(model = llm_model_config.GPT.model_name,   
                        messages = [{"role":"system","content":prompt}], 
                        frequency_penalty = 0, 
                        temperature=0,  
                        presence_penalty = 0)
        # print("response: ",response)
        if isinstance(response, str):
            response = json.loads(response)
        # result = response.replace(": null",': ""')
        # parsed_result = eval(result)['choices'][0]['message']['content']
        parsed_result = response['choices'][0]['message']['content']
        return parsed_result

    # @retry_with_exponential_backoff
    async def a_generate(self, prompt: str) -> str:
        """
        Args: (prompt: The prompt for calculation of the Alignment and Coverage scores)

        Returns: (result from the self.invoke() method)
        """
        chat_model = self.load_model()
        return self.invoke(chat_model,prompt)





class AnswerRelevanceScore:
    
    def __init__(self):
        pass
        
    def _getscore(self, dataDict):
        """
        Args: (dataDict: input JSON)

        Returns: (resultObj: AnswerRelevancyResult data object having corresponding filled values)
        """
        self.dataDict = InputData(**dataDict).dict()
        question = self.dataDict['question']
        answer = self.dataDict['answer']

        test_case = LLMTestCase(
          input=question, 
          actual_output=answer
        )

        de_model = GPTModel_OpenAI(model = llm_model_config.GPT.model_name)
        answer_relevance_metric = AnswerRelevancyMetric(
            model = de_model
        )

        result = evaluate([test_case], [answer_relevance_metric])

        scores = result[0].metrics[0].score
        reason = result[0].metrics[0].reason
        resultObj = AnswerRelevancyResult(**{"score":scores,"reason":reason})

        return resultObj

