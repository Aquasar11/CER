from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv(override=True)  # Reads .env file and loads environment variables

# list of different settings to run
multi_run_configs = {

    "Ours + Temp + + P + log": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "sum"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + * P + log": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + H + log": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + * P + min": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'min',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + * P + max": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'max',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + * P + h_mean": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'h_mean',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + H + weighted_mean": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'weighted_mean',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + H + min": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'min',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + H + h_mean": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'h_mean',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + H + max": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'max',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + * P + last": {
        "decoding_mode": 'last',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },

    "Ours + Temp + H + last": {
        "decoding_mode": 'last',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        # Options: "default", "sum", "entropy",
        "confidence": "entropy"
    },

    "Ours + Temp + * P + weighted_mean": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'weighted_mean',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },


    "Ours + Temp + * P + weighted_half": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'weighted_half',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },


    "Ours + Temp + * P + weighted_2": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        "baseline_cot": "k-seperate",
        "scoring_mode": 'weighted_2',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default"  # Options: "default", "sum", "entropy",
    },



    ############ baselines ##########

    "Self Const": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true]
        "baseline_cot": 'self_consistency',
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "default",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "P_True": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true]
        "baseline_cot": "p_true",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "Greedy": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true]
        "baseline_cot": "GREEDY",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "greedy",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "Predictive Entropy": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true, PE, NL, NE]
        "baseline_cot": "PE",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "Normilized-length Likelihood": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true, PE, NL, NE]
        "baseline_cot": "NL",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "Likelihood": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true, PE, NL, NE, LL]
        "baseline_cot": "LL",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

    "Normalized-length Entropy": {
        "decoding_mode": 'all',  # "all": all the numbers "last": the last number
        # [k-seperate, self_consistency, p_true, PE, NL, NE]
        "baseline_cot": "NE",
        "scoring_mode": 'log',  # log, min, max, h_mean, mean, weighted_mean
        # "temperature": temperature sampling  "greedy": greedy sampling
        "sampling_mode": "temperature",
        "confidence": "top_2_diff",  # Options: "default", "sum", "entropy",
        "use_base_prompt": True,
    },

}


# general configuration
@dataclass
class Config:
    model_name: str = os.getenv("MODEL_NAME",
                                "meta-llama/Llama-3.1-8B-Instruct")  # Path to the HuggingFace model or local directory
    data_dir = os.getenv("DATA_DIR", "data")
    # Load the model from the local directory instead of the HF.
    read_model_from_huggingface: bool = eval(
        os.getenv("LOCAL_MODEL", 'True'))
    hugging_face_token: str = os.getenv(
        "HUGGING_FACE_TOKEN", "")  # Huggingface Token

    # specify the running mode "all" that means all of them.
    run_name: str = os.getenv("RUN_NAME", "Ours + Temp + * P + weighted_mean")
    # number of chains in self-consistency
    K: int = int(os.getenv("K", 10))
    aggregate: bool = True  # True: aggregate paths False: the best path
    multihop: bool = eval(os.getenv("MULTIHOP", 'False'))
    
    # Number of samples to process
    number_samples: int = int(os.getenv("N_SAMPLE", 500))
    seed: int = int(os.getenv("SEED", 11))  # Seed for shuffling the dataset
    step_decomposition: bool = eval(os.getenv("STEP_DECOMPOSITION", 'False'))

    gsm8k_shots: str = "inputs/shots/gsm8k.txt"  # path to shots of gsm8k
    allenai_shots: str = "inputs/shots/allenai.txt"  # path to shots of allenai
    math_shots: str = "inputs/shots/math.txt"  # path to shots of math
    hotpot_shots: str = "inputs/shots/hotpot.txt"  # path to shots of hotpot
    trivia_shots: str = "inputs/shots/trivia.txt"  # path to shots of trivia

    datasets = eval(os.getenv("DATASETS", """{
        "allenai": "allenai_math_qa_test_processed.parquet",
        "math": "src_datasets_math_dataset_test_processed.parquet",
        "gsm8k": "openai_gsm8k_test_processed.parquet",
        "hotpot": "hotpotqa_processed.parquet",
        "trivia": "triviaqa_processed.parquet",
    }"""))

    batch_size = int(os.getenv("BATCH_SIZE", 1))
