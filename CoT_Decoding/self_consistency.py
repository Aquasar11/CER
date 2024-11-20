import logging
from difflib import SequenceMatcher
import torch
from transformers import PreTrainedModel, PreTrainedTokenizer
from typing import List, Tuple, Dict, Optional
import re

logger = logging.getLogger(__name__)


class AdvancedSelfConsistency:
    def __init__(self, model, tokenizer, num_samples: int = 10, similarity_threshold: float = 0.8):
        self.model = model
        self.tokenizer = tokenizer

        # Set pad_token_id if it's not set
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.num_samples = num_samples
        self.similarity_threshold = similarity_threshold

    def generate_responses(self, message: str) -> List[str]:
        input_ids = self.tokenizer.encode(message, return_tensors="pt").to(self.device)
        attention_mask = torch.ones_like(input_ids).to(self.device)

        responses = []
        probs = []
        for _ in range(self.num_samples):
            output = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=512,
                num_beams=1,
                temperature=1.0,
                top_p=1.0,
                repetition_penalty=1.0,
                length_penalty=1.0,
                no_repeat_ngram_size=0,
                early_stopping=False,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                output_scores=True,
                return_dict_in_generate=True,
            )

            generated_sequence = output.sequences[0]
            answer_ids = generated_sequence[len(input_ids[0]):]
            answer_text = self.tokenizer.decode(answer_ids, skip_special_tokens=True)
            probs.append(output)

            responses.append(answer_text)
        return responses

    def calculate_similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    def cluster_similar_responses(self, responses: List[str]) -> List[List[str]]:
        clusters = []
        for response in responses:
            added_to_cluster = False
            for cluster in clusters:
                if self.calculate_similarity(response, cluster[0]) >= self.similarity_threshold:
                    cluster.append(response)
                    added_to_cluster = True
                    break
            if not added_to_cluster:
                clusters.append([response])
        return clusters

    def aggregate_results(self, responses: List[str]) -> Dict[str, any]:
        final_answers = responses
        clusters = self.cluster_similar_responses(final_answers)

        cluster_info = []
        for cluster in clusters:
            cluster_info.append({
                "answer": cluster[0],
                "frequency": len(cluster),
                "variants": cluster
            })

        cluster_info.sort(key=lambda x: x['frequency'], reverse=True)

        return {
            "clusters": cluster_info,
            "total_responses": len(responses),
            "num_unique_clusters": len(clusters)
        }

    def evaluate(self, prompt: str, mode: str) -> Dict[str, any]:
        responses = self.generate_responses(prompt)

        if mode == "baseline":
            aggregated_result = self.aggregate_results(responses)

            return {
                "individual_responses": responses,
                "aggregated_result": aggregated_result
            }

        # elif decoding_mode == "new":
        #     # Extract all numerical values
        #     all_numerical_values = extract_all_numerical_values(answer_text)
        #     if all_numerical_values:
        #         confidence_sum = 0.0
        #         total_valid_values = 0
        #         for num_value in all_numerical_values:
        #             num_value_ids = tokenizer.encode(num_value, add_special_tokens=False)
        #
        #             # Find the start index of the final occurrence of the numerical value in the answer_ids
        #             answer_ids_list = answer_ids.tolist()
        #             num_value_ids_list = num_value_ids
        #
        #             num_value_start_idx = -1
        #             for i in range(len(answer_ids_list) - len(num_value_ids_list) + 1):
        #                 if answer_ids_list[i:i + len(num_value_ids_list)] == num_value_ids_list:
        #                     num_value_start_idx = i - 1  # because the first generated token's score is not presented in output.scores
        #
        #             if num_value_start_idx == -1:
        #                 continue
        #
        #             num_value_scores = output.scores[num_value_start_idx: num_value_start_idx + len(num_value_ids)]
        #
        #             # Calculate confidence score (Δ) for this numerical value
        #             confidence_sum += calculate_confidence_for_final_answer(num_value_scores,
        #                                                                     torch.tensor(num_value_ids, device=device))
        #             total_valid_values += 1
        #
        #         if total_valid_values > 0:
        #             confidence = confidence_sum / total_valid_values
        #             final_answer = all_numerical_values[
        #                 -1]  # Consider the last numerical value as the final answer for consistency
        #             paths.append((answer_text, confidence, final_answer))
        #
        # if aggregate_paths:
        #     return aggregate_paths_based_on_scores(paths)
        # else:
        #     return max(paths, key=lambda x: x[1])


def extract_last_numerical_value(text: str) -> Optional[str]:
    """
    Extract the last numerical value from a given text.

    Args:
        text: The text from which to extract the numerical value.

    Returns:
        The last numerical value if found, otherwise None.
    """
    matches = re.findall(r'\b\d+\.?\d*\b', text)
    return matches[-1] if matches else None


def extract_all_numerical_values(text: str) -> List[str]:
    """
    Extract all numerical values from a given text.

    Args:
        text: The text from which to extract numerical values.

    Returns:
        A list of all numerical values found in the text.
    """
    return re.findall(r'\b\d+\.?\d*\b', text)


def calculate_confidence_for_final_answer(logits: List[torch.Tensor], answer_ids: torch.Tensor) -> float:
    """
    Calculate the confidence score (Δ) as specified in the paper.

    Args:
        logits: List of logits for each decoding step
        answer_ids: Tensor of token ids for the answer

    Returns:
        Confidence score (Δ)
    """
    confidence_sum = 0.0
    valid_tokens = 0
    for t, token_id in enumerate(answer_ids):
        if t >= len(logits):
            break
        token_logits = logits[t]
        probs = torch.softmax(token_logits, dim=-1)
        if probs.size(-1) > 1:
            top_2_probs, _ = torch.topk(probs, min(2, probs.size(-1)))
            if top_2_probs.size(-1) > 1:
                confidence_sum += (top_2_probs[-1][0] - top_2_probs[-1][1]).item()
            else:
                confidence_sum += 1.0  # Max confidence if there's only one token
        else:
            confidence_sum += 1.0  # Max confidence if there's only one token
        valid_tokens += 1

    return confidence_sum / valid_tokens if valid_tokens > 0 else 0.0


def aggregate_paths_based_on_scores(paths: List[Tuple[str, float, str]]) -> Tuple[str, float, str]:
    """Aggregate multiple paths based on their confidence scores."""
    answer_scores = {}
    best_full_ans = None
    best_full_ans_delta = -1
    for answer, delta, final_answer in paths:
        answer_scores[final_answer] = answer_scores.get(final_answer, 0) + delta
        if best_full_ans_delta < delta:
            best_full_ans_delta = delta
            best_full_ans = answer
    best_answer = max(answer_scores, key=answer_scores.get)
    return best_full_ans, answer_scores[best_answer], best_answer


def self_consistency_decode(
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        messages: List[Dict[str, str]],
        k: int = 10,
        aggregate_paths=False,
        decoding_mode: str = "baseline",
) -> Tuple[str, float, str]:
    """
    Implement CoT-decoding for a given chat input.

    Args:
        model: The Hugging Face transformer model.
        tokenizer: The associated tokenizer.
        messages: List of chat messages in the format [{"role": "user", "content": "..."}]
        k: The number of alternative tokens to consider at the first step.

        decoding_mode: Mode of decoding, either "baseline" or "new".

    Returns:
        A tuple containing the best path (or aggregated result) and its confidence score.
    """

    # Use the chat template to format the input
    if tokenizer.chat_template:
        input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        # Fallback for tokenizers without chat templates
        input_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        input_text += "\nassistant:"

    self_consistency = AdvancedSelfConsistency(model, tokenizer, num_samples=k)
    result = self_consistency.evaluate(input_text, mode=decoding_mode)

    return result

    # logger.info("Advanced Self-Consistency Results:")
    # logger.info(f"Total responses: {result['aggregated_result']['total_responses']}")
    # logger.info(f"Number of unique clusters: {result['aggregated_result']['num_unique_clusters']}")
    # for i, cluster in enumerate(result['aggregated_result']['clusters'], 1):
    #     logger.debug(f"\nCluster {i}:")
    #     logger.debug(f"  Representative answer: {cluster['answer']}")
    #     logger.debug(f"  Frequency: {cluster['frequency']}")
    #     logger.debug(f"  Variants: {cluster['variants']}")
