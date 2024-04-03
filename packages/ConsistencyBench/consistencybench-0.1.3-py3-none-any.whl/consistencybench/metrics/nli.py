import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class NLI:
    """
    Allows for determining it two sentences contradict
    each other or if one sentence entails the other.

    Parameters:
        tok_path (str): Path to the tokenizer.
        model_path (str): Path to the model.
        max_length (int): Maximum length of the input sequences.
    """

    def __init__(
        self,
        tok_path="microsoft/deberta-base-mnli",
        model_path="microsoft/deberta-base-mnli",
    ):
        self.detection_tokenizer = AutoTokenizer.from_pretrained(tok_path)
        self.detection_model = AutoModelForSequenceClassification.from_pretrained(
            model_path
        )
        self.cuda_flag = torch.cuda.is_available()
        if self.cuda_flag:
            self.detection_model.to("cuda")


class Entailment(NLI):
    name = "entailment"

    def score(self, sentence1, sentence2):
        """
        Determines if the first sentence entails the second.

        Parameters:
            sentence1 (str): The first sentence.
            sentence2 (str): The second sentence.

        Returns:
            (float): Probability that sentence1 entails sentence2.
        """
        inputs = self.detection_tokenizer(
            sentence1, sentence2, return_tensors="pt", padding=True
        )
        if self.cuda_flag:
            inputs.to("cuda")
        outputs = self.detection_model(**inputs)
        scores = outputs.logits.softmax(dim=-1)
        return scores.T[2].item()
    
    def score_two_sided(self, sentence1, sentence2):
        return max(self.score(sentence1, sentence2), self.score(sentence2, sentence1))


class Contradiction(NLI):
    name = "contradiction"
    
    def score(self, sentence1, sentence2):
        """
        Determines if the first sentence contradicts the second.

        Parameters:
            sentence1 (str): The first sentence.
            sentence2 (str): The second sentence.

        Returns:
            (float): Probability that sentence1 contradicts sentence2.
        """
        inputs = self.detection_tokenizer(
            sentence1, sentence2, return_tensors="pt", padding=True
        )
        if self.cuda_flag:
            inputs.to("cuda")
        outputs = self.detection_model(**inputs)
        scores = outputs.logits.softmax(dim=-1)
        return scores.T[0].item()

    def score_two_sided(self, sentence1, sentence2):
        return min(self.score(sentence1, sentence2), self.score(sentence2, sentence1))
