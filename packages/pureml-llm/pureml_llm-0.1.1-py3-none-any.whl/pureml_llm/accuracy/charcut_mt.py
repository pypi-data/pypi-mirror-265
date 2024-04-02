from pureml_llm.metric_base import MetricBase
from typing import Any
from charcut import calculate_charcut



class Charcut(MetricBase):
    name: Any = 'charcut'
    input_type : Any = 'text'
    output_type : Any = 'float'
    kwargs: Any = {}


    def parse_data(self,data):
        return data 
    

    def compute(self,references,predictions):
        """
                    Calculates how good predictions are given some references.
            Args:
                predictions: a list of predictions to score. Each prediction should be a string with
                tokens separated by spaces.
                references: a list of reference for each prediction. Each reference should be a string with
                tokens separated by spaces.
            Returns:
                charcut_mt: the CharCut score
            Examples:
                >>> from charcut_mt import Charcut
                >>> charcut_mt = Charcut()
                >>> preds = ["this week the saudis denied information published in the new york times",
                ...          "this is in fact an estimate"]
                >>> refs = ["saudi arabia denied this week information published in the american new york times",
                ...         "this is actually an estimate"]
                >>> charcut_mt.compute(references=refs, predictions=preds)
                {'charcut_mt': 0.1971153846153846}
        """
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                charcut_mt = calculate_charcut(references, predictions)
                return {self.name: charcut_mt[0]}
            except Exception as e:
                print(e)
    

    def risk(self,scores):
        threshold = 0.8
        return {self.name : 'pass' if scores[self.name] > threshold else 'fail'}