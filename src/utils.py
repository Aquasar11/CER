import re

import pandas as pd
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

# load the model and its tokenizer
def load_model_and_tokenizer(model_name):
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        local_files_only=False,
        device_map='cuda',
        torch_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer


# load the dataset
def load_and_sample_dataset(dataset_name, split, subset = None, sample_size = None, seed = None):    
    if subset is None:
        dataset = load_dataset(dataset_name, split=split)
    else:
        dataset = load_dataset(dataset_name, split)[subset]

    if sample_size is not None and seed is not None:
        dataset = dataset.shuffle(seed=seed).select(range(sample_size))

    return dataset


# construct prompt for given question
def construct_prompt(question, few_shot=True, few_shot_path=None):
    if few_shot: # few-shot setting
        few_shots = read_from_txt(few_shot_path)
        base_prompt = few_shots.format(question=question)
        return base_prompt
    else: # zero-shot setting
        pass


# extract the last numerical value from a given text
def extract_last_numerical_value(text):
    matches = re.findall(r'\b\d+\.?\d*\b', text)
    return matches[-1] if matches else None

# extract all numerical values from a given text
def extract_all_numerical_values(text):
    return re.findall(r'\b\d+\.?\d*\b', text)

# write content in a file_path
def write_to_txt(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# read content from a file_path
def read_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# save results in a csv file
def save_results_to_csv(results, filename):
    results_df = pd.DataFrame(results)
    results_df.to_csv(filename, index=False)


# print the final accuracy
def print_final_accuracy(description, accuracy):
    print(f"Final Accuracy for {description}: {accuracy:.2f}%")