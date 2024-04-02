from bert_score import score
from pureml_llm.metric_base import MetricBase
from typing import Any


class BertScorePrecision(MetricBase):
    name: Any = 'bert_score_precision'
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
        precision_list = []
        recall_list = []
        precision = precision.tolist()
        #for i in range(len(precision)):
        #    precision_list = round(precision[i],2)
        recall = recall.tolist()
        #for i in range(len(recall)):
        #    recall_list = round(recall[i],2)

        f1 = f1.tolist()
        #for i in range(len(f1)):
        #    f1_list = round(f1[i],2)
        #print(type(precision))

        # return {
        #     self.name : {'precision' : precision,
        #                  'recall' : recall,
        #                  'f1' : f1}
        # }
        return {
            self.name: precision[0]
        }
    
    
    def risk(self,score):
        threshold = 0.7
        # precision_threshold = []
        # recall_threshold = []
        # f1_threshold = []
        # precision_pass = 0
        # precision_fail = 0
        # recall_pass = 0
        # recall_fail = 0
        # f1_pass = 0
        # f1_fail = 0
        # for i in range(len(score[self.name]['precision'])):
        #     if score[self.name]['precision'][i] >= threshold:
        #         precision_threshold.append('pass')
        #         precision_pass += 1
        #     else:
        #         precision_threshold.append('fail')
        #         precision_fail += 1
        # # for i in range(len(score[self.name]['recall'])):
        # #     if score[self.name]['recall'][i] >= threshold:
        # #         recall_threshold.append('pass')
        # #         recall_pass += 1
        # #     else:
        # #         recall_threshold.append('fail')
        # #         recall_fail += 1
        # # for i in range(len(score[self.name]['f1'])):
        # #     if score[self.name]['f1'][i] >= threshold:
        # #         f1_threshold.append('pass')
        # #         f1_pass += 1
        # #     else:
        # #         f1_threshold.append('fail')
        # #         f1_fail += 1
        
        # # precision_threshold = 'pass' if score[self.name]['precision'] == threshold else 'fail'
        # # recall_threshold = 'pass'  if score[self.name]['recall'] == threshold else 'fail'
        # # fmeasure_threshold  = 'pass' if score[self.name]['fmeasure'] == threshold else 'fail'
        # print(f"{precision_pass} passed, {precision_fail} failed from Precision")
        # # print(f"{recall_pass} passed, {recall_fail} failed from Recall")
        # # print(f"{f1_pass} passed, {f1_fail} failed from F1")

        # # return {
        # #     self.name : {'precision' : precision_threshold,
        # #                  'recall' : recall_threshold,
        # #                  'fmeasure' : f1_threshold}
        # # }
        # return {
        #     self.name: precision_threshold
        # }
        return {self.name: 'pass' if score[self.name] >= threshold else 'fail'}