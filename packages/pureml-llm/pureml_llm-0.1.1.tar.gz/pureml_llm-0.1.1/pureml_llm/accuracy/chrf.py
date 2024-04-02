from typing import Any 
from pureml_llm.metric_base import MetricBase 
from sacrebleu import CHRF 



class Chrf(MetricBase):
    name: Any = 'chrf'
    input_type: Any = 'text'
    output_type: Any = 'float'
    kwargs: Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions,char_order = 6, word_order = 0, beta = 2,lowercase = False):
        """
        Args:
            predictions (list of str): The predicted sentences.
            references (list of list of str): The references. There should be one reference sub-list for each prediction sentence.
            char_order (int): Character n-gram order. Defaults to `6`.
            word_order (int): Word n-gram order. If equals to `2`, the metric is referred to as chrF++. Defaults to `0`.
            beta (int): Determine the importance of recall w.r.t precision. Defaults to `2`.
            lowercase (bool): if `True`, enables case-insensitivity. Defaults to `False`.

        Returns:
            'score' (float): The chrF (chrF++) score,
            'char_order' (int): The character n-gram order,
            'word_order' (int): The word n-gram order. If equals to 2, the metric is referred to as chrF++,
            'beta' (int): Determine the importance of recall w.r.t precision

        Examples:
            Example 1--a simple example of calculating chrF:
                >>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
                >>> reference = [["The relationship between dogs and cats is not exactly friendly."], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
                >>> from chrf import Chrf
                >>> chrf = Chrf()
                >>> results = chrf.compute(predictions=prediction, references=reference)
                >>> print(results)
                {'score': 84.64214891738334, 'char_order': 6, 'word_order': 0, 'beta': 2}
        """

        if (len(references) != 0) and (len(predictions) != 0):
            try:
                references_per_prediction = len(references[0])
                transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]
                sb_chrf = CHRF(char_order, word_order, beta, lowercase)
                output = sb_chrf.corpus_score(predictions, transformed_references)
                return {self.name: output.score}
            
            except Exception as e:
                print(e)

    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}