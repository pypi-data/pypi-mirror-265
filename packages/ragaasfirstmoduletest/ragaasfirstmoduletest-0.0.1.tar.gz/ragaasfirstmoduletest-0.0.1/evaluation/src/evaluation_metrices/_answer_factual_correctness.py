
from LLMPrompts._prompts import ANSWER_FACTUAL_CORRECTNESS_PROMPT
from helper_files._gpt_chat_completion import GPTCompletion
from pydantic import BaseModel
import typing
import os
from helper_files import llm_model_config

os.environ["HUGGINGFACEHUB_API_TOKEN"] = llm_model_config.HF.api_token

class InData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    question: str
    answer: str
    ground_truth: str

class AFCResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines the proportion of true factual claims present in the LLM response compared to the ground truth"
    score: str
    reason: str = None



class AnswerFactualCorrectness:
    
    def __init__(self):
        
        self.prompt = ANSWER_FACTUAL_CORRECTNESS_PROMPT
    
    def _parse_prompt(self,question, answer, ground_truth):
        """
        Args: (question: 'question' value from input JSON,
              answer: 'answer' value from input JSON,
              ground_truth: 'ground_truth' value from input JSON)

        Returns: (prompt: Compiled prompt message to give for GPT chat completion)
        """
        prompt_content = self.prompt.replace("{question}",question).replace("{ground_truth}",ground_truth).replace("{answer}",answer)

        prompt = [{"role":"system","content":prompt_content}]
        return prompt
        
        
    def _getscore(self, dataDict):
        """
        Args: (dataDict: input JSON)

        Returns: (resultObj: AFCResult data object having corresponding filled values)
        """
        self.dataDict = InData(**dataDict).dict()
        question =  self.dataDict['question']
        answer = self.dataDict['answer']
        ground_truth = self.dataDict['ground_truth']
        
        prompt = self._parse_prompt(question, answer, ground_truth)
        
        gptObj = GPTCompletion(prompt)
        result = gptObj.getResult()
        result = result.replace(": null",': ""')
        parsed_result = eval(result)['choices'][0]['message']['content']
        try:

            if isinstance(parsed_result,dict):
                pass
            elif isinstance(parsed_result,str):
                parsed_result = eval(parsed_result)

            # print("result: ",parsed_result)
            
            score = parsed_result['Score']
            reason = parsed_result['Explanation']
            resultObj = AFCResult(**{'score':str(score),'reason':reason})

            return resultObj       

        except:
            print("Failed in parsing the result:\n")
            print(parsed_result)
            raise