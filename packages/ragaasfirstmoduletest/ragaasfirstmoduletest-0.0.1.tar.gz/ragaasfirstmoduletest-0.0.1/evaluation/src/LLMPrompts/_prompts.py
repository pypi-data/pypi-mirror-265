ANSWER_FACTUAL_CORRECTNESS_PROMPT = '''You are an experienced AI researcher specialised in Natural Language Processing (NLP). I am going to provide you with a metric called Answer factual completeness (AFC) for evaluating retrieval augmented generation (RAG). I am going to provide the formula, explanation and step by step explanation for the same.  You need to understand the metric and apply it to the new dataset that I am going to provide. Below are the details.  
Answer factual Completeness (AFC):
This metric evaluates if the answer (A) captures all the factual information present in the ground truth (G).
Formula:
AC = (Number of factual claims in Answer (A) matching Ground Truth (G)) / (Total number of factual claims in Ground Truth (G))
Explanation:
AC measures how many factual details from the ground truth are included in the answer. It focuses on completeness, not necessarily the order or phrasing.
Below is the Step-by-Step procedure:
1. Identify Factual Claims in Ground Truth (G)
2.Identify Factual Claims in Answer (A)
3. Match Claims  by comparing each factual claim in the answer (A) with the corresponding claim(s) in the ground truth (G).
4. Assign Completeness Scores by comparing all the facts in G and A. For all the facts in G do the following: If a claim that is present in G is also present in A then assign a value of '1', else assign '0'
5. Calculate the AFC score using the above formula. 

You need to provide proper justification for your score.
Given the answer, ground_truth and the question calculate the AC score and reason for giving the score\n\n

"answer": {answer}
"ground_truth": {ground_truth}
"question": {question}

Output in STRICTLY in valid JSON format with following key value pairs:
"Score": score
"Explanation":reason for score


output:  '''


ANSWER_CORRECTNESS_PROMPT = '''Extract following from given question and ground truth
            "TP": statements that are present in both the answer and the ground truth,
            "FP": statements present in the answer but not found in the ground truth,
            "FN": relevant statements found in the ground truth but omitted in the answer, 
        
Output STRICTLY in only valid JSON format.

question: "What powers the sun and what is its primary function?"
answer: "The sun is powered by nuclear fission, similar to nuclear reactors on Earth, and its primary function is to provide light to the solar system."
ground_truth: "The sun is actually powered by nuclear fusion, not fission. In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy. This energy is what lights up the sun and provides heat and light, essential for life on Earth. The sun's light also plays a critical role in Earth's climate system and helps to drive the weather and ocean currents."
Extracted statements: {"TP": ["The sun's primary function is to provide light"], "FP": ["The sun is powered by nuclear fission", "similar to nuclear reactors on Earth"], "FN": ["The sun is powered by nuclear fusion, not fission", "In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy", "This energy provides heat and light, essential for life on Earth", "The sun's light plays a critical role in Earth's climate system", "The sun helps to drive the weather and ocean currents"]}

question: "What is the boiling point of water?"
answer: "The boiling point of water is 100 degrees Celsius at sea level."
ground_truth: "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit) at sea level, but it can change with altitude."
Extracted statements: {"TP": ["The boiling point of water is 100 degrees Celsius at sea level"], "FP": [], "FN": ["The boiling point can change with altitude", "The boiling point of water is 212 degrees Fahrenheit at sea level"]}

question: {question}
answer: {answer}
ground_truth: {ground_truth}
Extracted statements: 

'''

RTS_PROMPTS = {'PROMPT_FOR_RELEVANCE' : '''Score the following Summary given the corresponding Article with respect to relevance from one to five, where one indicates "irrelevance", and five indicates "perfect relevance". Note that relevance measures the Summary\'s selection of important content from the Article, whether the Summary grasps the main message of the Article without being overwhelmed by unnecessary or less significant details.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score.\nOutput in only valid JSON format.\n\n{"reason": "", "score": ""}''',
'PROMPT_FOR_CONSISTENCY' : '''Score the following Summary given the corresponding Article with respect to consistency from one to five, where one indicates "inconsistency" and five indicates "perfect consistency". Note that consistency measures the factual alignment between the Summary and the Article, whether the Summary is faithful to the Article without introducing contradictions or misleading representations.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score.\nOutput in only valid JSON format.\n\n{"reason": "", "score": ""}''',
'PROMPT_FOR_FLUENCY': '''Score the following Summary given the corresponding Article with respect to fluency from one to five, where one indicates "disfluency" and five indicates "perfect fluency". Note that fluency measures the quality of individual sentences in the Summary, whether the Summary is well-written, grammatically correct, and readable on the sentence level.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score.\nOutput in only valid JSON format.\n\n{"reason": "", "score": ""}''',
'PROMPT_FOR_COHERENCE': '''Score the following Summary given the corresponding Article with respect to coherence from one to five, where one indicates "incoherence" and five indicates "perfect coherence". Note that coherence measures the collective quality of the Summary, whether the Summary presents information that flows smoothly and avoids abrupt transitions or disjoint statements.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score.\nOutput in only valid JSON format.\n\n{"reason": "", "score": ""}'''}


QAG_PROMPTS = {'alignment':{
		"SYSTEM_PROMPT" : "You are a smart LLM output evaluator. I will provide you the rules to evaluate the LLM output and set of instruction to evaluate LLM output.",
		"USER_PROMPT" : "Are you clear about your role?",
		"ASSISTANT_PROMPT" : "Sure, I'm ready to help you with your LLM output evaluation task. Please provide me with the necessary information to get started.",
		"FINAL_PROMPT" : 
'''Rules for LLM output evaluation:
You will be given with the answer text and ground truth. Please follow these to generate the evaluation
1. Extract all claims made in an answer  text
2. For each claim, ask the ground truth whether it agrees ('yes') or not ('no') with the claim made.
3. calculate the proportion (0-1) of claims in an LLM output that are accurate and consistent with the ground truth. this will be called as QAG score.
4. If answer text has no claims or language states text similar to ' documents do not provide information', return the score as '0'

Below is the required data:

LLM_output: {}
Ground_truth: {}

Output the response STRICTLY in valid json format with follwing key pairs:
'QAG_Score': QAG Score
'Reason': Give the explaination for QAG score

output: '''
		},
	'coverage': {
		"SYSTEM_PROMPT" : "You are a smart LLM output evaluator. I will provide you the rules to evaluate the LLM output and set of instruction to evaluate LLM output.",
		"USER_PROMPT" : "Are you clear about your role?",
		"ASSISTANT_PROMPT" : "Sure, I'm ready to help you with your LLM output evaluation task. Please provide me with the necessary information to get started.",
		"FINAL_PROMPT" : 
'''Rules for LLM output evaluation:
1. Extract all claims made in ground truth text
2. For each claim, ask the LLM output text it agrees ('yes') or not ('no') with the claim made.
3. calculate the proportion (0-1) of claims in an ground truth text that are accurate and consistent with the LLM output text. this will be called as QAG score
4. If LLM output text has no claims or language states text similar to 'documents do not provide information', return the score as '-1'.
5. If ground truth text has no claims, return score as '0'.

Below is the required data:

LLM_output: {}
Ground_truth: {}

Output the response STRICTLY in valid json format with follwing key pairs:
'QAG_Score': QAG Score
'Reason': Give the explaination for QAG score

output: '''
		}
}

ANSWER_TRUENESS_PROMPT = '''You are an expert researcher in AI. You need to provide some novel techniques to evaluate the responses generated by LLM. You are provided with the following. Answer provided by the LLM (A), Ground truth(G). Please provide proper justification for the reasoning. 
You need to do the following:
1. Generate questions for all the factual claims in Ground truth.
2. For each generated question, you need to check if the question is answered in given answer. If the question is answered then return "1", otherwise "0".
3. Calculate the final score according to the given formula:
score= Sum of the questions which returned "1"/ Total number of factual questions.
4. provider explaination for score
explanation: You need to provide explanation for the score by checking if all the factual claims in G are answered in A. You need to provide the factual claims which are answered and which are not answered.

Below is the data you can use:
ground_truth: {ground_truth}
answer: {answer}


Output the response STRICTLY in valid JSON format with following keys pairs:
"score": calculated score
"explanation":explaination for score

output: '''


ANSWER_COMPLETENESS_PROMPT = '''I am defining a new Retrieval Augment Metric(RAG) metric for the inference or reasoning use case. You need to understand the metric explanation carefully and apply it to the sample data that I provide. You are provided with the following: Q -User query, G -Ground truth, A - Answer that is provided by LLM. 
 
 
Here is the details of the new metric.
 
Metric Name: Answer Completeness
Explanation: This metric assesses how cohesive the LLM's answer (A) is to the original user query (Q).
Evaluation Criteria : If the answer is covering all parts of the ground truth, then you can consider the answer as “fully completeness” else you can consider as “partially complete”
 
 
Based on the above explanation, You need to provide a value for the metric for evaluating the answer A for a given query Q based on the Ground truth G.
You need to assign a score for answer completeness on a scale of 1 to 10, where 1 being the lowest and 10 being the highest. You need to provide proper justification for your score.\n\n

Below is the data you can use:
question: {question}
ground_truth: {ground_truth}
answer: {answer}



Output the resopnse STRICTLY in valid JSON format with following key pairs:
"score": score for answer completeness
"explanation": justification for score

output: '''