from pureml_llm.metric_base import MetricBase
from typing import Any
from cer import calculate_cer


class Character(MetricBase):
    name: Any = 'character'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}

    def parse_data(self,data):
        return data
    
    def compute(self,references,predictions):
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                scores = calculate_cer(references, predictions)
                return {self.name: scores}
            except Exception as e:
                print(e)

    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'} 


