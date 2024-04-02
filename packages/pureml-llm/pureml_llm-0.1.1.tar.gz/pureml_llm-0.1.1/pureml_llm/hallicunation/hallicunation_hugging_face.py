from transformers import pipeline
from pureml_llm.metric_base import MetricBase
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Any

model = AutoModelForSequenceClassification.from_pretrained('vectara/hallucination_evaluation_model')
tokenizer = AutoTokenizer.from_pretrained('vectara/hallucination_evaluation_model')

pipe = pipeline("text-classification", model="vectara/hallucination_evaluation_model")


class HallucinationMetric(MetricBase):
    name: Any = 'Hallucination'
    input_type: Any = 'text'
    output_type : Any = None
    kwargs: Any = {}

    def parse_data(self, data):
        return data
    

    def compute(self,references,predictions,**kwargs):
        if type(references) == str:
            references = [references]
        if type(predictions) == str:
            predictions = [predictions]
        

        pairs = [(references[i],predictions[i]) for i in range(len(references))]
        
        #print(f"Pairs: {pairs}")
        model.eval()

        inputs = tokenizer.batch_encode_plus(pairs, return_tensors='pt', padding=True)

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits.cpu().detach().numpy()
            # convert logits to probabilities
            scores = 1 / (1 + np.exp(-logits)).flatten()

        
        #print(f"Hallucination Scores: {scores}")
        return {
            self.name : round(float(scores[0]),2)
        }



    def risk(self,score):

        threshold = 0.5
        print(f"Score: {score}")
        print(f"type of Score: {type(score)}")
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}