import os
import numpy as np
import typing as t
import logging
import pysbd
from tqdm import tqdm

from helper_files import llm_model_config


os.environ["HUGGINGFACEHUB_API_TOKEN"] = llm_model_config.HF.api_token 

logger = logging.getLogger(__name__)
from datasets import Dataset 
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings

seg = pysbd.Segmenter(language="en", clean=False)

class AnswerSimilarity:
    def __init__(self,dataDict: t.Dict):
        self.dataDict = dataDict
        self.embeddings =  LangchainEmbeddingsWrapper(HuggingFaceEmbeddings(model_name='BAAI/bge-base-en'))

    
    def calculate(self):
        scores = []
        for row in tqdm(self.dataDict):

            ground_truth = t.cast(str, row["ground_truth"])
            answer = t.cast(str, row["answer"])
            embedding_1 = np.array( self.embeddings.embed_text(ground_truth))
            embedding_2 = np.array( self.embeddings.embed_text(answer))
            # Normalization factors of the above embeddings
            norms_1 = np.linalg.norm(embedding_1, keepdims=True)
            norms_2 = np.linalg.norm(embedding_2, keepdims=True)
            embedding_1_normalized = embedding_1 / norms_1
            embedding_2_normalized = embedding_2 / norms_2
            similarity = embedding_1_normalized @ embedding_2_normalized.T
            score = similarity.flatten()
            assert isinstance(score, np.ndarray), "Expects ndarray"
            score = score.tolist()[0]
            scores.append(score)
        return {"answer_similarity":scores}
    

    async def calculate_row(self,row):
        # scores = []
        # for row in tqdm(self.dataDict):
        ground_truth = t.cast(str, row["ground_truth"])
        answer = t.cast(str, row["answer"])
        embedding_1 = await np.array( self.embeddings.embed_text(ground_truth))
        embedding_2 = await np.array( self.embeddings.embed_text(answer))
        # Normalization factors of the above embeddings
                  
        norms_1 =  await np.linalg.norm(embedding_1, keepdims=True)
        norms_2 =  await np.linalg.norm(embedding_2, keepdims=True)
        embedding_1_normalized = embedding_1 / norms_1
        embedding_2_normalized = embedding_2 / norms_2
        similarity = embedding_1_normalized @ embedding_2_normalized.T
        score = similarity.flatten()
        assert isinstance(score, np.ndarray), "Expects ndarray"
        score = score.tolist()[0]
        return score