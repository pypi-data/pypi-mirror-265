from transformers.models.auto.modeling_auto import AutoModelForSequenceClassification
from transformers.models.auto.tokenization_auto import AutoTokenizer
from pureml_llm.metric_base import MetricBase
from typing import Any
import torch
from .progess_bar import tqdm_wrapper

_fluency_model_path = "prithivida/parrot_fluency_model"
_fluency_tokenizer = None
_fluency_model = None


class Fluency(MetricBase):
    name: Any = 'fluency'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions,**kwargs):

        """
        Calculates fluency score of predictions using the Parrot Fluency model from Hugging Face.

        Args:
            references (str): The reference text. (also called prompt to LLMs)
            predictions (str): The predicted text. (also called as output of LLMs)
        
            predictions are only used in the computation of fluency and references are not used.
        Returns:
           dict : A dictionary containing the fluency as key and it's respective score as value.
        
        """
        if predictions is None:
            raise ValueError("Predictions cannot be None")

        if predictions is not None:
            try:
                scores = fluency_local(predictions)
                return {self.name: scores}
            except Exception as e:
                print(e)

    

    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}
        




def fluency_local(predictions):

    global _fluency_tokenizer, _fluency_model_path

    if _fluency_tokenizer is None or _fluency_model  is None:
        _fluency_tokenizer = AutoTokenizer.from_pretrained(_fluency_model_path)

    _fluency_model = AutoModelForSequenceClassification.from_pretrained(_fluency_model_path)


    input_tokens = _fluency_tokenizer(predictions,return_tensors="pt",padding=True)

    batch_size = 8 
    scores = []
    with torch.no_grad():
         for i in tqdm_wrapper(range(0, len(predictions), batch_size),
                              total=(len(predictions) + batch_size - 1) //
                              batch_size):
            batch_input_tokens = {
                k: v[i:i + batch_size] for k, v in input_tokens.items()
            }
            # Probabilities of [negative, neutral, positive]
            probs = torch.nn.functional.softmax(
                _fluency_model(**batch_input_tokens).logits, dim=1)
            scores.extend(probs[:, 1].tolist())
    return scores[0]
    
