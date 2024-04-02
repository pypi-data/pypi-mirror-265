import os
import numpy as np
import typing as t
import logging
import openai
from tenacity import retry

import pysbd
from tqdm import tqdm


logger = logging.getLogger(__name__)
from datasets import Dataset 
from ragas.embeddings import BaseRagasEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from ._answer_similarity import AnswerSimilarity

from LLMPrompts._prompts import ANSWER_CORRECTNESS_PROMPT
from pydantic import BaseModel
from helper_files._gpt_chat_completion import GPTCompletion


class InData(BaseModel):
    """
    Defining the data types for data validation. 
    The data initialized through this class should meet all the data type criteria else it will lead to DataValidationError
    """
    question: str
    answer: str
    ground_truth: str


class AnswerCorrectnessResult(BaseModel):
    """
    Define the output data object
    description: About the metric
    score: Metric value
    reason: Reason for assigning the value
    """
    description: str = "This metric defines the correctness of LLM response based on the query, compared to the ground truth"
    score: float
    reason: str = None



class AnswerCorrectness:
    def __init__(self):

        self.prompt = ANSWER_CORRECTNESS_PROMPT
        self.embeddings =  HuggingFaceEmbeddings(model_name='BAAI/bge-base-en')


    def _compute_statement_presence(self, prediction: t.Any) -> float:
        """
        Args: (prediction: generated response from GPT chat completion)

        Returns: (score: answer correctness score)
        """
        assert GPTCompletion is not None, "LLM must be set"

        key_map = [
            "TP",
            "FP",
            "FN",
        ]
        if prediction:
            if isinstance(prediction,str):
                prediction = eval(prediction)

            prediction = [prediction.get(k, np.nan) for k in key_map]
            tp, fp, fn = [
                len(item) if isinstance(item, list) else np.nan for item in prediction
            ]
            if any([np.isnan(i) for i in [tp, fp, fn]]):
                score = np.nan
                logger.warning(
                    "Invalid prediction format. Expected a list of dictionaries with keys 'TP', 'FP', 'FN'"
                )
            else:
                score = tp / (tp + 0.5 * (fp + fn)) if tp > 0 else 0
        else:
            score = np.nan

        return score



    
    async def _getscore(self,dataDict):
        """
        Args: (dataDict: input JSON)

        Returns: (resultObj: AnswerCorrectnessResult data object having corresponding filled values)
        """
        self.dataDict = InData(**dataDict).dict()
        self.answerSimilarity = AnswerSimilarity(dataDict)
        prompt = self.prompt.replace("{answer}",self.dataDict['answer']).replace("{question}",self.dataDict['question']).replace('{ground_truth',self.dataDict['ground_truth'])
        gptObj = GPTCompletion([{"role":"system","content":prompt}])
        result = gptObj.getResult()
        result = result.replace(": null",': ""')
        generated_text = eval(result)['choices'][0]['message']['content']
        if generated_text:
            f1_score = self._compute_statement_presence(generated_text)
            assert self.answerSimilarity is not None, "AnswerSimilarity must be set"

            similarity_score =  await self.answerSimilarity.calculate_row(self.dataDict)
            # similarity_score = similarity_score['answer_similarity'][0]
            score = np.average(
            [f1_score, similarity_score],
            weights=[0.75, 0.25],
        )
            score = float(score)
        else:
            score = None
        # return {"answer_correctness":score}
        value = score
        resultObj = AnswerCorrectnessResult(**{"score":value})

        return resultObj

