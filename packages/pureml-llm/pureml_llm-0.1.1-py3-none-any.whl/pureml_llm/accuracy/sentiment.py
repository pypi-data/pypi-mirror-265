from transformers.models.auto.modeling_auto import AutoModelForSequenceClassification
from transformers.models.auto.tokenization_auto import AutoTokenizer
from pureml_llm.metric_base import MetricBase
from typing import Any
import torch
from .progess_bar import tqdm_wrapper


_sentiment_model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
_sentiment_tokenizer = None
_sentiment_model = None


class Sentiment(MetricBase):
    name: Any = 'sentiment'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions):
        """
        calculates the sentiment of the predictions using cardiffnlp/twitter-roberta-base-sentiment-latest model from Hugging Face.

        Args:
            references (str) : The reference text. (also called prompt to LLMs)
            predictions (str) : The predicted text. (also called as output of LLMs)

            references are not used in the computation of sentiment and only predictions are used.
        """

        if predictions is None:
            raise ValueError("Predictions cannot be None")

        if predictions is not None:
            try:
                scores = sentiment_local(predictions)
                return {self.name: scores}
            except Exception as e:
                print(e)


    def  risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}



def sentiment_local(predictions):
    global _sentiment_tokenizer, _sentiment_model

    if _sentiment_tokenizer is None or _sentiment_model is None:
        _sentiment_tokenizer = AutoTokenizer.from_pretrained(
            _sentiment_model_path)

        
    _sentiment_model = (AutoModelForSequenceClassification.
                                from_pretrained(_sentiment_model_path))

    input_tokens = _sentiment_tokenizer(predictions,
                                        return_tensors='pt',
                                        padding=True)

    with torch.no_grad():
        probs = torch.nn.functional.softmax(
            _sentiment_model(**input_tokens).logits, dim=1)

    return (probs[:, 1] / 2 + probs[:, 2]).tolist()[0]