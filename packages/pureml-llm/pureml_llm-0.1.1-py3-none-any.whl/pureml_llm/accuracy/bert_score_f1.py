from bert_score import score
from pureml_llm.metric_base import MetricBase
from typing import Any


class BertScoreF1(MetricBase):
    name: Any = 'bert_score_f1'
    input_type: Any = 'text'
    #output_type = 'score'
    output_type: Any = None
    kwargs: Any = {}

    def parse_data(self,data):
        return data 
    
    def compute(self,references,predictions,**kwargs):
        if type(references) == str:
            references = [references]
        if type(predictions) == str:
            predictions = [predictions]
        precision,recall,f1 = score(cands=references,refs=predictions,lang='en',verbose=True) #Can add model_type='xlnet-base-cased' as an argument

        # To convert tensors to list

        f1 = f1.tolist()


        return {
            self.name : f1[0]
        }
    
    
    def risk(self,score):
        threshold = 0.7
        precision_threshold = []
        recall_threshold = []
        f1_threshold = []
        precision_pass = 0
        precision_fail = 0
        recall_pass = 0
        recall_fail = 0
        f1_pass = 0
        f1_fail = 0
        
        # for i in range(len(score[self.name]['f1'])):
        #     if score[self.name]['f1'][i] >= threshold:
        #         f1_threshold.append('pass')
        #         f1_pass += 1
        #     else:
        #         f1_threshold.append('fail')
        #         f1_fail += 1
        
        # print(f"{f1_pass} passed, {f1_fail} failed from F1")

        # return {
        #     self.name : f1_threshold
        # }

        return {self.name : "pass" if score[self.name] >= threshold else "fail"}