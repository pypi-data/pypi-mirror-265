from bert_score import score
from pureml_llm.metric_base import MetricBase
from typing import Any


class BertScoreRecall(MetricBase):
    name: Any = 'bert_score_recall'
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
        
        recall_list = []
        recall = recall.tolist()
        return {
            self.name : recall[0]
        }
    
    
    def risk(self,score):
        threshold = 0.7
        recall_threshold = []
        # recall_pass = 0
        # recall_fail = 0
        # for i in range(len(score[self.name]['recall'])):
        #     if score[self.name]['recall'][i] >= threshold:
        #         recall_threshold.append('pass')
        #         recall_pass += 1
        #     else:
        #         recall_threshold.append('fail')
        #         recall_fail += 1
        
        # print(f"{recall_pass} passed, {recall_fail} failed from Recall")
        
        # return {
        #     self.name : recall_threshold
        # }
        return {
            self.name : "pass" if score[self.name] >= threshold else "fail"
        }