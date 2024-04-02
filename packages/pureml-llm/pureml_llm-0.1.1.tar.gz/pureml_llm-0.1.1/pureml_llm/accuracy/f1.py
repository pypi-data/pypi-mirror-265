from pureml_llm.metric_base import MetricBase
from typing import Any
import nltk
from nltk.metrics import scores


class F1(MetricBase):
    name: str = 'f1'
    input_type: str = 'text'
    output_type: Any = None
    kwargs: Any = {}


    def parse_data(self,data):
        return data 
    

    def calculate_f1(self,candidate, reference):
        """Calculates F1 score for candidate against reference"""

        # Tokenize candidate and reference
        cand_tokens = nltk.word_tokenize(candidate)
        ref_tokens = nltk.word_tokenize(reference)

        # Convert both to sets
        cand_set = set(cand_tokens)
        ref_set = set(ref_tokens)

        # Calculate TP, FP, FN
        tp = len(cand_set.intersection(ref_set))
        fp = len(cand_set - ref_set)
        fn = len(ref_set - cand_set)

        # Calculate precision and recall
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        
        # Calculate F1 score
        return (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0)

    
    def compute(self,references,candidates):
        """Evaluates candidates against reference texts"""
        scores = []
        for i, candidate in enumerate(candidates):
            reference = references[i]
            score = self.calculate_f1(candidate, reference)
            scores.append(score)

        return {
             self.name : round(score,2)
        }                                       
    
    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}