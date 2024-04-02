from pureml_llm.metric_base import MetricBase
from typing import Any
from fuzzywuzzy import fuzz
import numpy as np


class RR10(MetricBase):
    name: str = 'rr_10'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}

    def parse_data(self,data):
      return data

    def reciprocal_rank(self,rank):
        return 0 if rank == 0 else 1.0/rank

    def rr_at_10(self,predictions, references):

        rr = []
        for prediction in predictions:
    
        # Get similarities between prediction and references
            similarities = [fuzz.token_sort_ratio(prediction, ref) for ref in references]
    
        # Get rank based on maximum similarity 
            rank = similarities.index(max(similarities)) + 1 

            rr.append(self.reciprocal_rank(rank))

        # Return mean reciprocal rank
        return np.mean(rr)

    def compute(self,references,predictions,**kwargs):

        score  = self.rr_at_10(references=references,predictions = predictions)

        return {
            self.name : score
        }
    
    def risk(self,score):
        #rr_risk = []
        threshold = 0.7
        return {self.name : 'pass' if score[self.name] >= threshold else 'fail'}