from pureml_llm.metric_base import MetricBase
from typing import Any 
from nltk.translate import meteor_score
from nltk import word_tokenize

class Meteor(MetricBase):
    name: Any = 'Meteor'
    input_type: Any = 'string'
    output_type: Any = 'float'
    kwargs: Any = {}


    def parse_data(self,data):
        return data 
    

    def compute(self,references,predictions):
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                references = word_tokenize(references[0])
                predictions = word_tokenize(predictions[0])
                score = meteor_score.single_meteor_score(references, predictions)
                return {self.name: score}
            except Exception as e:
                print(e)
                
    def risk(self,scores):
        threshold = 0.8
        return {self.name: "pass" if scores[self.name] > threshold else "fail"}