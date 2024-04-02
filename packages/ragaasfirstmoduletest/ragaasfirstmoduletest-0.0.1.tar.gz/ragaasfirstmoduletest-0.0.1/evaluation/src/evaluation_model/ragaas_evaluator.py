import logging
from copy import deepcopy
from deepeval.test_case import LLMTestCase

import time
import os
import nest_asyncio
nest_asyncio.apply()

from helper_files.ragaas_constants import Default_Output_Values
from helper_files.utils import exception_handler
from deepeval.metrics import SummarizationMetric
from openai import OpenAI
from deepeval.models import GPTModel
from typing import Optional
import asyncio

from evaluation_metrices._alignment_coverage_score import AlignmentCoverageScore
from evaluation_metrices._answer_completeness import AnswerCompletenessScore
from evaluation_metrices._answer_correctness import AnswerCorrectness
from evaluation_metrices._answer_factual_correctness import AnswerFactualCorrectness
from evaluation_metrices._answer_relevancy import AnswerRelevanceScore
from evaluation_metrices._answer_similarity import AnswerSimilarity
from evaluation_metrices._answer_trueness import AnswerTrueness
from evaluation_metrices._qag_method import QAG_Metric
from evaluation_metrices._rts_method import ReasonThenScore

#from evaluation_metrices._mcq_method import 




qag_metric_alignment = QAG_Metric(score_type = 'alignment')
qag_metric_coverage = QAG_Metric(score_type = 'coverage')                                         #working
alignment_coverage_metric = AlignmentCoverageScore()            #working
answer_trueness_metric = AnswerTrueness()                       #working
answer_factual_correctness_metric = AnswerFactualCorrectness()  # working
answer_relevancy_metric = AnswerRelevanceScore() # working

# TODO
#answer_correctness_metric  = AnswerCorrectness()      #parsing error
#answer_similarity_metric_score = AnswerSimilarity() 
# answer_correctness_score  = AnswerCorrectness()  # done
# #answer_factual_correctness_score = AnswerFactualCorrectness()  # not working
# answer_similarity_metric_score = AnswerSimilarity()  # working



class Evaluator:
    def __init__(self, conf):
        self.conf = conf


    def get_required_metrics(self):
        req_metrics = [k for k, v in self.conf['metrics'].items() if v ==True]
        req_metrics.remove('create')
        print("*"*150)
        logging.info(f"________Evaluation Model Execution: The required metrics are- {req_metrics}________")
        print("*"*150)
        return req_metrics

    @exception_handler()
    def execute(self, df):
        logging.info("****************Running Evaluation Model Execution Pipeline****************")
        df_eval = deepcopy(df)
        if (len(df_eval) < 1):
            logging.info(f"______Evaluation Model Execution: Empty dataframe input to the Evaluator class______")
            return

        # 1. get the list of evaluation metric to be calculated from config
        req_metrics = ["qags"]          # Hardcoding this for release 1.0.1
        # req_metrics = self.get_required_metrics()

        # instantiating the null string as values for required metrics column
        for column in req_metrics:
            # if column == 'alignment':
            #     df_eval['Alignment'] = ''
            #     df_eval['Coverage'] = ''
            if column == 'qags':
                df_eval['qags_alignment'] = ''
                df_eval['qags_coverage'] = ''
                # df_eval['qags_alignment_reason'] = ''
                # df_eval['qags_coverage_reason'] = ''
                
            else:
                df_eval[column] = ''

        # df_eval[req_metrics] = ''
        # # instantiating the null string as values for required metrics column
        # df_eval['qags_alignment'] = ''
        # df_eval['alignment_coverage_score'] = ''
        # df_eval['answer_factual_correctness_score'] = ''
        # df_eval['answer_relevancy_score'] = ''
        # df_eval['alignment_score'] = ''
        # df_eval['coverage_score'] = ''


        # iterate through each row of dataframe and get the evaluation metrics
        for idx, row in df_eval.iterrows():
            if idx==5:
                return df_eval

            question= row[self.conf['golden_dataset']['question']]
            ground_truth= row[self.conf['golden_dataset']['ground_truth']]
            answer= row[self.conf['golden_dataset']['llm_output']]

            input_1 = {
                        "question":question,
                        "ground_truth":ground_truth,
                        "answer":answer, 
                    }

            input_2 = {
                            "answer":answer,
                            "ground_truth":ground_truth   
                        }

            input_3 = {
                            "question":question,
                            "answer":answer
                        }

            if 'qags' in req_metrics:
                try:
                    # create the test qag object
                    # calculate qag_metric_alignment_score          
                    qag_metric_alignment_score = qag_metric_alignment._getscore(input_2)
                    logging.info(f"qags_alignment score: {qag_metric_alignment_score.score}")
                    logging.info(f"qags_alignment reason: {qag_metric_alignment_score.reason}")
                    # update the values in df
                    df_eval.loc[idx, 'qags_alignment'] = qag_metric_alignment_score.score
                    df_eval.loc[idx, 'qags_alignment_reason'] = qag_metric_alignment_score.reason
                except Exception as e:
                    logging.exception("Evaluation Model Execution:Error occurred while processing qags_alignment")
                    # TODO- add default values logic here
                    df_eval.loc[idx, 'qags_alignment'] = Default_Output_Values.Not_Available
                    df_eval.loc[idx, 'qags_alignment_reason'] = Default_Output_Values.Not_Available


                # calculate qag_metric_coverage_score 
                try:
                    qag_metric_coverage_score = qag_metric_coverage._getscore(input_2)
                    logging.info(f"qags_coverage score: {qag_metric_coverage_score.score}")
                    logging.info(f"qags_coverage reason: {qag_metric_coverage_score.reason}")
                    # update the values in df
                    df_eval.loc[idx, 'qags_coverage'] = qag_metric_coverage_score.score
                    df_eval.loc[idx, 'qags_coverage_reason'] = qag_metric_coverage_score.reason
                except Exception as e:
                    logging.exception("Evaluation Model Execution:Error occurred while processing qags_coverage")
                    # TODO- add default values logic here
                    df_eval.loc[idx, 'qags_coverage'] = Default_Output_Values.Not_Available
                    df_eval.loc[idx, 'qags_coverage_reason'] = Default_Output_Values.Not_Available

            # if ('alignment' in df_eval.columns) or ('coverage' in df_eval.columns):

            #     alignment_coverage_score = alignment_coverage_metric._getscore(input_2)  #working
            #     if ('alignment' in df_eval.columns):
            #         logging.info(f"Alignment Score: {alignment_coverage_score.score['Alignment']}")
            #         df_eval.loc[idx, 'Alignment'] = alignment_coverage_score.score['Alignment']
            #     if ('coverage' in df_eval.columns):
            #         logging.info(f"Coverage Score: {alignment_coverage_score.score['Coverage']}")
            #         df_eval.loc[idx, 'Coverage'] = alignment_coverage_score.score['Coverage']
            #     time.sleep(5)

            # tagging correctness from config to answer_factual_correctness_score
            if 'answer_factual_correctness_metric' in req_metrics:
                answer_factual_correctness_score = answer_factual_correctness_metric._getscore(input_1)  ## working
                logging.info(f"answer_factual_correctness_metric: {answer_factual_correctness_score.score}")
                df_eval.loc[idx, 'answer_factual_correctness_metric'] = answer_factual_correctness_score.score
                time.sleep(5)

            # tagging relevancy from config to answer_relevancy_score
            if 'relevancy' in req_metrics: 
                answer_relevancy_score = answer_relevancy_metric._getscore(input_3)
                logging.info(f"relevancy (answer_relevancy_score): {answer_relevancy_score.score}")
                df_eval.loc[idx, 'relevancy'] = answer_relevancy_score.score
                time.sleep(5)

            # tagging completeness from config to answer_trueness_score
            if 'answer_trueness_metric' in req_metrics:
                answer_trueness_score = answer_trueness_metric._getscore(input_2)
                logging.info(f"answer_trueness_score: {answer_trueness_score.score}")
                df_eval.loc[idx, 'answer_trueness_score'] = answer_trueness_score.score
                time.sleep(5)


        logging.info("****************Model Execution Pipeline Run Completed****************")
        return df_eval




