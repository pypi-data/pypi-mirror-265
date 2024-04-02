from pureml_llm.metric_base import MetricBase
from typing import Any
from fuzzywuzzy import fuzz


class QuasiExactMatch(MetricBase):
    name: str = 'quasi_exact_match'
    input_type: str = 'text'
    output_type: Any = None
    kwargs: Any = {}

    def parse_data(self,data):
        return data 
    

    def calculate_quasi_match_score(self,references, predictions):
        """Calculates quasi-exact match between candidate and reference"""
        # Get fuzzy token set ratio between candidate and reference
        ratio = fuzz.token_sort_ratio(predictions, references)
        
        # Calculate score between 0 and 1
        return ratio / 100 
    
    def compute(self,references,predictions,**kwargs):
            """Evaluates candidates against reference texts"""
            scores = []
            for i, candidate in enumerate(predictions):
                reference = references[i]
                score = self.calculate_quasi_match_score(candidate, reference)
                scores.append(score)

            return {
                 self.name : scores[0]
            }
    
    def risk(self,score):
        threshold  = 0.8
        risk_score = []
        fail_count = 0
        pass_count = 0
        for i in range(len(score[self.name])):
                if threshold == score[self.name][i]:
                   risk_score.append('pass')
                   pass_count += 1
                else:
                    risk_score.append('fail')
                    fail_count += 1
        print(f"{pass_count} passed, {fail_count} failed from Quasi Exact Match")
        
        return {self.name :  risk_score[0]}
