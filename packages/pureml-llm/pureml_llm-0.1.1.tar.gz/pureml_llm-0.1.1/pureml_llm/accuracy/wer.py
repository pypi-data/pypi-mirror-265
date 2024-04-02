from pureml_llm.metric_base import MetricBase
from jiwer import wer,compute_measures
from typing import Any


class WER(MetricBase):
    name: Any = ' wer'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}




    def parse_data(self,data):
        return data
    


    def compute(self,references,predictions):
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                incorrect = 0
                total = 0
                for prediction, reference in zip(predictions, references):
                    measures = compute_measures(reference, prediction)
                    incorrect += measures['substitutions'] + measures['deletions'] + measures['insertions']
                    total += measures['substitutions'] + measures['deletions'] + measures['hits']
                scores = incorrect / total
                return {self.name: scores}
            except Exception as e:
                print(e)

    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}