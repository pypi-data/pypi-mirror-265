from typing import List,Any
from nltk.translate import gleu_score 
from pureml_llm.metric_base import MetricBase
from .tokenizer_13a import Tokenizer13a


class GoogleBLUE(MetricBase):
    name: Any = 'GoogleBLEU'
    input_type: Any = 'text'
    output_type: Any = 'text'
    kwargs: Any = {}


    def parse_data(self,data):
        return data 
    

    def compute(self,references,predictions):
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                tokenizer = Tokenizer13a()
                references = [tokenizer(reference) for reference in references]
                predictions = [tokenizer(prediction) for prediction in predictions]
                score = gleu_score.corpus_gleu(references,predictions)
                return {self.name: round(score,2)}
        
            except Exception as e:
                print(e)
    
    def risk(self,scores):
        threshold = 0.8
        return {self.name: "pass" if scores[self.name] > threshold else "fail"}