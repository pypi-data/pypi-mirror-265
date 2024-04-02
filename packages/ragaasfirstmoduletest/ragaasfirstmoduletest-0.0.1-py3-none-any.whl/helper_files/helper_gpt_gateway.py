""" helper function for calling openAI GPT using LLM gateway
"""
import time
import os
from typing import Optional, List, Dict
from pathlib import Path
import json
import re
import openai
from openai import OpenAI
import pandas as pd
import tiktoken


RUN_UNKNOWN_ERROR_LOGIC = False
UNKNOWN_COUNT = 10
DEFAULT_HEADERS = {"apiversion": "2023-07-01-preview"}


GPT_MODEL_MAPPING = {}
GPT_MODEL_MAPPING["gpt-4-turbo-1106-preview"] = {
    "model": "gpt-4-turbo-1106-preview",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-turbo-0125-preview"] = {
    "model": "gpt-4-turbo-0125-preview",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-32k-0613"] = {
    "model": "gpt-4-32k-0613",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-8k-0613"] = {
    "model": "gpt-4-8k-0613",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-8k-0613_perf"] = {
    "model": "gpt-4-8k-0613",
    "api_base": "https://perf-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-35-turbo-0613"] = {
    "model": "gpt-35-turbo-0613",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-35-turbo-16k-0613"] = {
    "model": "gpt-35-turbo-16k-0613",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["text-embedding-ada-002"] = {
    "model": "text-embedding-ada-002",
    "api_base": "https://uat-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-8k-0613_dev"] = {
    "model": "gpt-4-8k-0613",
    "api_base": "https://dev-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-4-32k-0613_dev"] = {
    "model": "gpt-4-32k-0613",
    "api_base": "https://dev-dsmbrsvc.anthem.com/llmgateway/openai",
}
GPT_MODEL_MAPPING["gpt-35-turbo_dev"] = {
    "model": "gpt-35-turbo",
    "api_base": "https://dev-dsmbrsvc.anthem.com/llmgateway/openai",
}


dir_path = Path(__file__).resolve().parent
os.environ["SSL_CERT_FILE"] = str(dir_path / "cert.pem")


def call_openai_gateway(
    token_id: str,
    prompt: str = None,
    sys_prompt: str = None,
    messages=None,
    model=None,
    engine="gpt3",
    temperature=0,
    max_tokens=500,
    debug=True,
    return_all=False,
    function_call=None,
    functions=None,
    **kwargs,
) -> str:
    """use LLM Gateway to call openai ChatCompletion function

    Args:
        token_id (str): your LLM gatway token ID
        prompt (str): user prompt
        sys_prompt (Optional[str], optional): system prompt. Defaults to None.
        messages (Optional[List[Dict[str, str]]], optional): messages combine user and system prompts.
                If not None, the messages wil take precedance over 'prompt' input
        engine (str, optional): GPT model. Defaults to "gpt3".
        temperature (int, optional): temperature for GPT model. Defaults to 0.
        max_tokens (int, optional): max token for GPT model. Defaults to 100.
        debug (bool, optional): Defaults to False.

    Returns:
        str: LLM output
    """

    ## refer to GPT_MODEL_MAPPING for model mapping
    if model is None:
        model = engine
    assert model in GPT_MODEL_MAPPING, "check your engine"

    api_base = GPT_MODEL_MAPPING[model]["api_base"]
    client = OpenAI(base_url=api_base, api_key=token_id, default_headers=DEFAULT_HEADERS)

    if debug:
        print(f"api key set as {token_id}")
        print(f"api base set as {api_base}")

    if messages is None:
        if sys_prompt:
            messages = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt},
            ]
        else:
            messages = [{"role": "user", "content": prompt}]

    if function_call is None:
        response = client.chat.completions.create(
            model=GPT_MODEL_MAPPING[model]["model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
    else:
        response = client.chat.completions.create(
            model=GPT_MODEL_MAPPING[model]["model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=functions,
            function_call=function_call,
            **kwargs,
        )

    if debug:
        print(response)
    response = json.loads(response)

    if return_all:
        return response

    llm_output = response["choices"][0]["message"]["content"]
    return llm_output


def embeddings_openai_gateway(
    token_id: str, text: str, engine: str = "text-embedding-ada-002", debug=True
) -> List[float]:
    """functions to robustly openai embeddings API

    Args:
        token_id (str): your LLM gateway token ID
        text (str): text that you want to embed
        engine (str): OpenAI embeddings engine

    Returns:
        List[float]: embeddings for text
    """
    assert engine in GPT_MODEL_MAPPING, "check your engine"

    api_base = GPT_MODEL_MAPPING[engine]["api_base"]
    client = OpenAI(base_url=api_base, api_key=token_id, default_headers=DEFAULT_HEADERS)

    if debug:
        print(f"api key set as {token_id}")
        print(f"api base set as {api_base}")

    response = client.embeddings.create(model=engine, input=text)
    if debug:
        print(response)
    assert isinstance(response, openai.types.create_embedding_response.CreateEmbeddingResponse)
    response = json.loads(response.model_dump_json(indent=2))
    embeddings = response["data"][0]["embedding"]
    return embeddings


def robust_call_openai_gateway(
    token_id: str,
    sys_prompt: str,
    prompt: str,
    engine: str,
    temperature: float,
    max_tokens: int = 500,
    sleep_time: int = 1,
    verbose: bool = True,
    debug: bool = False,
    summary_key: str = None,
    exception_prompt: str = None,
    return_all: bool = False,
    **kwargs,
) -> str:
    """functions to robustly call openai

    Args:
        token_id (str): your LLM gateway token ID
        sys_prompt (str): prompt to define GPT system role
        prompt (str): user content prompt
        engine (str): GPT engine
        temperature (float): temperature for GPT
        max_tokens (int, optional): max token for GPT model. Defaults to 500.
        sleep_time (int, optional): time in seconds between repeated attempts
        verbose (bool, optional): Defaults to True.
        summary_key(str, optional): which section to summary, only relavent to case summary
        exception_prompt(str, optional): retry-prompt when certain exception happens, only relavent to case summary

    Returns:
        str: string output from GPT
    """
    flag = True
    counter = 0
    while flag:
        try:
            response = call_openai_gateway(
                token_id=token_id,
                sys_prompt=sys_prompt,
                prompt=prompt,
                engine=engine,
                temperature=temperature,
                max_tokens=max_tokens,
                debug=debug,
                timeout=100,
                return_all=return_all,
                **kwargs,
            )
            if not return_all:
                print("d2 Got a response from API!")
            elif response["responseCode"] == 200:
                print("d1 Got a response from API!")
            else:
                raise Exception(response["Error"].split(".")[0])
            if RUN_UNKNOWN_ERROR_LOGIC:
                if return_all:
                    if response["choices"][0]["message"].get("function_call", None) is not None:
                        llm_output = response["choices"][0]["message"]["function_call"]["arguments"]
                    else:
                        llm_output = response["choices"][0]["message"]["content"]
                else:
                    llm_output = response
                if llm_output is not None:
                    if len(llm_output) and llm_output.count("unknown") >= UNKNOWN_COUNT and summary_key:
                        print("Initiating LLM call for unknown error!")
                        response = call_openai_gateway(
                            token_id=token_id,
                            sys_prompt=sys_prompt,
                            prompt=exception_prompt,
                            engine=engine,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            debug=debug,
                            return_all=return_all,
                            **kwargs,
                        )
                else:
                    print("Response received as None while attempting unknown logic")
            flag = False

        except Exception as exception:
            counter += 1
            if verbose:
                if "choices" in f"{exception}":
                    if counter == 200:
                        print(exception)
                        print("No response in 200 seconds.")
                        return "No response from gateway"
                    if not (counter % 20):
                        print(counter)
                        print("Still haven't received a response from API yet...")
                else:
                    print(f"\n\n\n{exception}\n\n\n")
            time.sleep(sleep_time)
    return response


def robust_chat_openai_gateway(
    token_id: str,
    messages: List[Dict[str, str]],
    engine: str,
    temperature: float,
    max_tokens: int = 500,
    sleep_time: int = 1,
    verbose: bool = True,
    debug: bool = False,
) -> str:
    """functions to robustly call ChatCompletion function of openai API

    Args:
        token_id (str): your LLM gateway token ID
        messages (List[Dict[str, str]]): message input for ChatCompletion
        engine (str): GPT engine
        temperature (float): GPT temperature
        max_tokens (int, optional): max token for GPT model. Defaults to 100.
        sleep_time (int, optional): time in seconds between repeated attempts
        verbose (bool, optional): Defaults to True.

    Returns:
        str: GPT output
    """
    flag = True
    counter = 0
    while flag:
        try:
            response = call_openai_gateway(
                token_id=token_id,
                prompt=None,
                messages=messages,
                engine=engine,
                temperature=temperature,
                max_tokens=max_tokens,
                debug=debug,
            )
            print("Got a response from API!")
            flag = False
        except Exception as exception:
            counter += 1
            if verbose:
                if "choices" in f"{exception}":
                    if counter == 20:
                        print("Haven't received a response from API yet...")
                    if not (counter % 20):
                        print("Still haven't received a response from API yet...")
                else:
                    print(f"\n\n\n{exception}\n\n\n")
            time.sleep(sleep_time)

    return response


def robust_embeddings_openai_gateway(
    token_id: str,
    text: str,
    engine: str = "text-embedding-ada-002",
    verbose: bool = True,
) -> List[float]:
    """functions to robustly openai embeddings API

    Args:
        token_id (str): your LLM gateway token ID
        text (str): text that you want to embed
        engine (str): OpenAI embeddings engine
        verbose (bool, optional): Defaults to True.

    Returns:
        List[float]: embeddings for text
    """

    flag = True
    while flag:
        try:
            embeddings = embeddings_openai_gateway(token_id, text, engine)
            flag = False
        except Exception as exception:
            if verbose:
                print(f"\n\n\n{exception}\n\n\n")
            time.sleep(1)
    return embeddings


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string.

    Args:
        string (str): input string
        encoding_name (str, optional): Defaults to "cl100k_base".

    Returns:
        int: number of token
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def parse_table(text: str, columns: List[str]) -> pd.DataFrame:
    """parse string input as pandas dataframe

    Args:
        text (str): input string
        columns (List[str]): list of expected column names

    Returns:
        pd.DataFrame: output dataframe
    """
    columns_regex = r"\|\s*" + r"\s*\|\s*".join(columns) + r"\s*\|\s*\n"
    columns_match = re.search(columns_regex, text)
    table = []
    if columns_match:
        rows = text[columns_match.end() :].split("\n")
        for row in rows:
            if len(row.strip()) == 0:
                continue
            row_regex = r"\|\s*" + r"\s*\|\s*".join([r"[^|]*" for c in columns]) + r"\s*\|\s*"
            if re.search(row_regex, row):
                row_split = [s.strip() for s in row.split("|")[1:-1]]
                if not row_split[0].strip("-"):  ## row with '----'
                    continue
                table.append(row_split)
            else:
                break
    else:
        return None

    table_df = pd.DataFrame(table, columns=columns)

    return table_df


def split_table_column(table_column: str) -> List[str]:
    """split input '|' seperated string as table column names

    Args:
        table_column (str): input string of column names seperated by '|'

    Returns:
        List[str]: List of column names
    """
    # Split the table column using the delimiter "|"
    split_columns = table_column.split("|")

    # Remove any leading/trailing white space from each column
    split_columns = [column.strip() for column in split_columns]

    # Remove any empty strings from the list
    split_columns = list(filter(None, split_columns))

    # Return the resulting list
    return split_columns


def chunckize(original: str, max_token=2048) -> List[str]:
    """Chunckize input string by '\n\n', each chunk max size < max_token

    Args:
        original (str): input string
        max_token (int, optional): max token size. Defaults to 2048.

    Returns:
        List[str]: output list of chuncks
    """
    para_list = original.split("\n\n")
    text_list = []
    rolling_str = ""

    for para in para_list:
        if num_tokens_from_string(rolling_str + para, "cl100k_base") > max_token:
            text_list.append(rolling_str)
            rolling_str = "\n\n"
        rolling_str += para + "\n\n"

    text_list.append(rolling_str)

    return text_list


def chunckize_overlap(original: str, overlap: int = 5, max_token=2048, separator="\n\n") -> List[str]:
    """Chunckize input string by '\n\n', each chunk max size < max_token
       take the last few pieces of previous chunck into chunck to create overlap

    Args:
        original (str): input string
        overlap (int, optional): overlap pieces (by '\n\n') between sequential chuncks.
            Defaults to 5.
        max_token (int, optional): max token number. Defaults to 2048.

    Returns:
        List[str]: output list of chuncks
    """

    para_list = original.split(separator)
    text_list = []
    rolling_str = ""

    for para in para_list:
        if num_tokens_from_string(rolling_str + para, "cl100k_base") > max_token:
            text_list.append(rolling_str)
            last_few = rolling_str.split("\n")[-overlap:]
            rolling_str = "\n".join(last_few)
        rolling_str += para + "\n"

    text_list.append(rolling_str)

    return text_list
