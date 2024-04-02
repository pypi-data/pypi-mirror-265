from pydantic import BaseModel,Extra
from typing import List,Dict, Any
import pandas as pd
import os
from .grade import Grade
from .schema import framework_list
from .frameworks import get_framework_details
from .assignments import assign_framework_to_model,update_assignments
from .reports import get_reports
import json
from rich import print
from pureml.utils.logger import get_logger
from pureml.components import dataset,model

logger = get_logger('pureml_llm.pureml_llm_eval.py')

os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Before importing TensorFlow






class Evaluation(BaseModel):
    input: List[str] = []
    output: List[str] =  []
    references: List[str]   = []
    metrics_list: Dict = {}
    framework_name: Any = None
    label_model: str
    label_dataset: str
    dataset: Any = None
    model: Any = None

    def framework_details(self):
        self.metrics_list = framework_list['pureml_genai'].keys()              # Kept Static to not have any dependency on the framework from backend.
        #metrics_data = get_framework_details(self.framework_name).keys()
        #self.metrics_list = [key.split('.')[-1] for key in metrics_data]
        #print(f"Metrics List: {self.metrics_list}")
        print("[bold green] Succesfully fetched the Metrics")
        logger.info(f"Succesfully fetched the Metrics: {self.metrics_list}")

    def load_dataset(self):
        self.dataset = dataset.fetch(self.label_dataset)
        if self.dataset:
            self.input = self.dataset['input']
            self.output = self.dataset['output']
            self.references = self.dataset['references']
            print(f"[bold green] Succesfully fetched the Dataset: {self.label_dataset}")
            logger.info(f"Succesfully fetched the Dataset: {self.label_dataset}")
        else:
            print(f"[bold red] Unable to fetch the Dataset: {self.label_dataset}")
            logger.error(f"Unable to fetch the Dataset: {self.label_dataset}")
            raise Exception(f"Unable to fetch the Dataset: {self.label_dataset}")
        
    def load_model(self):
        self.model = model.fetch(self.label_model)
        if self.model:
            print(f"[bold green] Succesfully fetched the Model: {self.label_model}")
            logger.info(f"Succesfully fetched the Model: {self.label_model}")
        else:
            print(f"[bold red] Unable to fetch the Model: {self.label_model}")
            logger.error(f"Unable to fetch the Model: {self.label_model}")
            raise Exception(f"Unable to fetch the Model: {self.label_model}")
        
    # def assigning_framework_to_model(self):
    #     sensitive_list = []
    #     assign_framework_to_model(framework_name = self.framework_name, label_model = self.label_model, sensitive_data = sensitive_list)

    
    def load(self):
        self.load_dataset()
        self.load_model()
        self.framework_details()
        #self.assigning_framework_to_model()

    

    def compute(self):
        grade = Grade(input = self.input, output = self.output, references = self.references, metrics_list = self.metrics_list)
        return grade.compute()
    

def evaluate(label_model: str, label_dataset:str,framework_name: str = None):
#def evaluate(input:str, output:str, references: str,  label_model: str, label_dataset: str,framework_name: str = None):
    #eval  = Evaluation(input = input, output = output, references = references, framework_name= framework_name,label_model = label_model,label_dataset=  label_dataset)
    try:
        eval = Evaluation(label_model = label_model,label_dataset=  label_dataset, framework_name= framework_name)
        eval.load()
        metrics_result = eval.compute()

        #return metrics_result
        result = {
            "model" : f"{label_model}",
            "dataset" : f"{label_dataset}",
            "data" : {
                "sensitive_columns" : [],
                "complete" : metrics_result,
                "subsets": []
            }
        }

        result  = json.dumps(result)
        status = update_assignments(data = result, label_model = label_model,framework_name = framework_name)
        if status:
            print("[bold green] Evaluation Completed Successfully & Data sent to Backend")
            logger.info(f"Evaluation Completed Successfully & Data sent to Backend")
        else:
            print("[bold red] Error in sending Data to Backend")
            logger.error(f"Error in sending Data to Backend")
        #get_reports(label_model,framework_name)
        return result
        #return metrics_result
    except Exception as e:
        logger.error(f"Error in Evaluation: {e}")
        print(f"Error in Evaluation: {e}")