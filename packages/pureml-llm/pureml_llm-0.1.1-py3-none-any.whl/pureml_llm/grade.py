from pydantic import BaseModel,Extra
from typing import List,Dict
from .accuracy_metrics_result import Accuracy
from .toxicity_metrics_result import Toxicity
from .hallicunation_metrics_result import Hallicunation
from .bias_metric_results import BiasMetricResult
from .metrics_import import accuracy_metrics, hallucination_metrics, bias_metrics, toxicity_metrics
from pureml.utils.logger import get_logger
logger = get_logger('pureml_llm.grade.py')

class Grade(BaseModel):
    output: List[str]                               # prediction = output
    input: List[str]
    references : List[str]                                    # references = input
    metrics_list: List = []
    scores: Dict = {}
    risk_scores: Dict = {}
    final_result: Dict = {}
    # metrics: Dict = {
    #     'accuracy' : Accuracy(),
    #     'hallicunation' : Hallicunation(),
    #     'bias' : BiasMetricResult(),
    #     'toxicity' : Toxicity()
    # }
    metrics: Dict = {}
    accuracy_list_from_policy: List = []
    hallucination_list_from_policy: List = []
    bias_list_from_policy: List = []
    toxicity_list_from_policy: List = []


    
    class Config:
        extra = Extra.ignore

    def load(self):
        accuracy_list = list(accuracy_metrics.keys())
        hallucination_list = list(hallucination_metrics.keys())
        bias_list = list(bias_metrics.keys())
        toxicity_list = list(toxicity_metrics.keys())

        self.accuracy_list_from_policy = []
        self.hallucination_list_from_policy = []
        self.bias_list_from_policy = []
        self.toxicity_list_from_policy = []

        for m in self.metrics_list:
            if m in accuracy_list:
                self.accuracy_list_from_policy.append(accuracy_metrics[m])
            elif m in hallucination_list:
                self.hallucination_list_from_policy.append(hallucination_metrics[m])
            elif m in bias_list:
                self.bias_list_from_policy.append(bias_metrics[m])
            elif m in toxicity_list:
                self.toxicity_list_from_policy.append(toxicity_metrics[m])
        
        self.metrics  = {
            "accuracy_metrics" : Accuracy(metrics = self.accuracy_list_from_policy),
            "hallucination" : Hallicunation(metrics = self.hallucination_list_from_policy),
            "bias" : BiasMetricResult(metrics = self.bias_list_from_policy),
            "toxicity" : Toxicity(metrics = self.toxicity_list_from_policy)
        }


    
    def compute(self):
        self.load()
        #print(f"self.metrics_list: {self.metrics_list}")
        #print(f"self.metrics: {self.metrics}")
        for m in self.metrics:
            if m == 'toxicity':
                if len(self.toxicity_list_from_policy) != 0:
                    logger.info(f"Computing Toxicity Metrics")
                    results = self.metrics[m].compute(predictions = self.output, api_key = "AIzaSyAI9xNklBLMW-2EEnlBJ8EkIgZHoiPK5b4",metrics = self.toxicity_list_from_policy)
                    #print(f"Results: {results}")
                    logger.info(f"Toxicity Metrics Results: {results}")
                    results  = {f"{k}": v for k, v in results.items()}
                    self.scores[m] = results
                    #self.scores[m] = f"{str(results)}"
            
            elif m == 'accuracy_metrics':
                if len(self.accuracy_list_from_policy) != 0:
                    logger.info(f"Computing Accuracy Metrics")
                    results = self.metrics[m].compute(references = self.references, predictions = self.output, metrics = self.accuracy_list_from_policy)
                    results  = {f"{k}": v for k, v in results.items()}
                    #print(f"Results: {results}")
                    logger.info(f"Accuracy Metrics Results: {results}")
                    self.scores[m] = results
                    #self.scores[m] = f"{str(results)}"

            elif m == 'hallucination':
                if len(self.hallucination_list_from_policy) != 0:
                    logger.info(f"Computing Hallucination Metrics")
                    results = self.metrics[m].compute(references = self.references, predictions = self.output,metrics = self.hallucination_list_from_policy)
                    results  = {f"{k}": v for k, v in results.items()}
                    logger.info(f"Hallucination Metrics Results: {results}")
                    #print(f"Results: {results}")
                    #self.scores[m] = f"{str(results)}"
                    self.scores[m] = results

            elif m == 'bias':
                if len(self.bias_list_from_policy) != 0:
                    logger.info(f"Computing Bias Metrics")
                    results = self.metrics[m].compute(references = self.references, predictions = self.output,metrics = self.bias_list_from_policy)
                    results  = {f"{k}": v for k, v in results.items()}
                    logger.info(f"Bias Metrics Results: {results}")
                    #print(f"Results: {results}")
                    #self.scores[m] = f"{str(results)}"
                    self.scores[m] = results
            #self.scores[m] = results
        
        #print(f"Line 66. self.scores : {self.scores}")
        #self.risk_scores = self.risk()     
        #return self.final()
        return self.scores
    
    def risk(self):
        for m in self.scores:
            #print(f"Line 45. self.scores[{m}] : {self.scores[m]}")
            try:
                self.risk_scores[m] = self.metrics[m].risk()
            except Exception as e:
                print(f"Error: {e}")
                try:
                    self.risk_scores[m] = self.metrics[m].risk(self.scores[m])
                except Exception as e:
                    print(f"Error: {e}") 
                
        #print(f"Line 46. self.risk : {self.risk_scores}")
        return self.risk_scores
    

    def final(self):
        self.final_result['scores'] = self.scores
        self.final_result['risk'] = self.risk_scores
        return self.final_result