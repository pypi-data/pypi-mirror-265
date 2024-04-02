import yaml
import sys
import os
from pathlib import Path

file_path = Path(__file__).resolve().parent

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.split(os.path.split(os.getcwd())[0])[0])
# print(sys.path)

with open(str(file_path / "gpt_config.yaml"), 'r') as f:
    config = yaml.safe_load(f)

from ._gpt_ import GPTConfig as GPT
from ._huggingface_ import HuggingFaceConfig as HF

f.close()