from fastapi import FastAPI, UploadFile, HTTPException, File,Form
from pydantic import BaseModel,Extra
from typing import List
from accuracy_metrics_result import Accuracy
from toxicity_metrics_result import Toxicity
from hallicunation_metrics_result import Hallicunation
from bias_metric_results import BiasMetricResult
import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Before importing TensorFlow


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return "Welcome to PureML, We are working on LLM Evaluation, PureML is an AI Goverance and Risk Management Platform"

class EvaluationRequest:
    def __init__(self, input: str, output: str):
        self.input = input
        self.output = output

class EvaluationRequest(BaseModel):
    output: List[str]                               # prediction = output
    input: List[str]
    references : List[str]                                # references = input
    #api_key: str 
    #text: List[str]

    class Config:
        extra = Extra.ignore

class ToxicityRequest(BaseModel):
    #api_key: str 
    text: str

    class Config:
        extra = Extra.ignore

@app.get('/')
def home():
    return "Hello Thrinadh, Let's start LLM Evaluation"


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper


@app.get('/evaluate')
async def evaluate_form():
    return FileResponse('static/index.html')

@app.post("/evaluate")
#@timer
def evaluate(request: EvaluationRequest):
    accuracy = Accuracy()
    hallicunation = Hallicunation()
    bias = BiasMetricResult()
    input_data  = request.input
    accuracy.references = request.output
    accuracy.predictions = request.references
    hallicunation.references = request.output
    hallicunation.predictions = request.input
    bias.references = request.output
    bias.predictions = request.input
    #toxicity = Toxicity()
    #toxicity.api_key = "AIzaSyAI9xNklBLMW-2EEnlBJ8EkIgZHoiPK5b4"
    #toxicity.text = request.text


    data =  {
            'category_score':   {
                accuracy.task_type : accuracy.compute(),
                hallicunation.task_type : hallicunation.compute(),
                bias.task_type : bias.compute()
                #toxicity.task_type : toxicity.compute()},
            },
            'risk_score': {
                accuracy.task_type : accuracy.risk(),
                hallicunation.task_type : hallicunation.risk(),
                bias.task_type : bias.risk()
                #toxicity.task_type : toxicity.risk()
            }
        }
    
    #return data

    input_data = request.input[0] if request.input else ""
    output_data = request.output[0] if request.output else ""
    references_data = request.references[0] if request.references else ""
    data_string = f"<b>Input: </b>{input_data}<br> <b> Output: </b> {output_data}"
    reference_string = f"<b>Reference: </b>{references_data}"
    
    category_score_data = data['category_score']['Accuracy']
    risk_score_data = data['risk_score']['Accuracy']
    Hallucination_score_data = data['category_score']['Hallucination']
    Hallucination_risk_score_data = data['risk_score']['Hallucination']
    bias_score_data = data['category_score']['Bias']
    bias_risk_score_data = data['risk_score']['Bias']

    print(f"bias_score_data: {bias_score_data}")
    print(f"bias_risk_score_data: {bias_risk_score_data}")

    # Formatting metrics into single strings for each metric column
    rouge_string = f"<b>Precision:</b> {category_score_data['rouge_score']['precision']} / {risk_score_data['rouge_score']['precision']}<br>" \
                   f"<b>Recall: </b>{category_score_data['rouge_score']['recall']} / {risk_score_data['rouge_score']['recall']}<br>" \
                   f"<b>F-Measure: </b>{category_score_data['rouge_score']['fmeasure']} / {risk_score_data['rouge_score']['fmeasure']}"
    
    bert_string = f"<b>Precision: </b>{category_score_data['bert_score']['precision'][0]} / {risk_score_data['bert_score']['precision'][0]}<br>" \
                  f"<b>Recall: </b>{category_score_data['bert_score']['recall'][0]} / {risk_score_data['bert_score']['recall'][0]}<br>" \
                  f"<b>F-Measure: </b>{category_score_data['bert_score']['f1'][0]} / {risk_score_data['bert_score']['fmeasure'][0]}"
    
    quasi_exact_match_string = f"<b>Score:</b> {category_score_data['quasi_exact_match'][0]} / {risk_score_data['quasi_exact_match'][0]}"
    f1_string = f"<b>Score: </b>{category_score_data['f1']} / {risk_score_data['f1']}"
    rr_10_string = f"<b>Score: </b>{category_score_data['rr_10']} / {risk_score_data['rr_10']}"
    hallucination_string = f"<b>Score: </b>{Hallucination_score_data['Hallucination']} / {Hallucination_risk_score_data['Hallucination']}"  
    bias_string = f"<b>Score: </b>{bias_score_data['bias']} / {bias_risk_score_data['bias']}"

    table_data = {
        'Data': [data_string],
        'Reference' : [references_data],
        'Rouge': [rouge_string],
        'BERT Score': [bert_string],
        'Quasi Exact Match': [quasi_exact_match_string],
        'F1': [f1_string],
        'RR 10': [rr_10_string],
        'Hallucination': [hallucination_string],
        'Bias' : [bias_string]
    }
    
    df = pd.DataFrame(table_data)
    html_table = df.to_html(classes='table table-striped', escape=False, index=False)  # escape=False to render HTML tags
    
    html_table = f"""
    <style>
        .table-container {{
            width: 100%;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 1rem;
        }}
        .table {{
            width: 100%;
            margin-bottom: 1rem;
            color: #212529;
            border-collapse: collapse;
        }}
        .table-striped tbody tr:nth-of-type(odd) {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
    </style>
    <div class="table-container">
        {html_table}
    </div>
    """
    
    return {"table": html_table}



@app.get("/toxicity")
async def toxicity_form():
    return FileResponse('static/toxicity.html')

@app.post("/toxicity")
async def toxicity_form(request: ToxicityRequest):
    toxic = Toxicity()
    toxic.api_key = "AIzaSyAI9xNklBLMW-2EEnlBJ8EkIgZHoiPK5b4"
    toxic.text = request.text
    data = {
        toxic.task_type: toxic.compute(),
        "RISK": toxic.risk()
    }
    input_data = request.text if request.text else ""
    data_string = f"<b>Input: </b>{input_data}<br> "
    
    category_score_data = data['Toxicity']
    risk_score_data = data['RISK']
    
    # Formatting metrics into single strings for each metric column
    profanity = f"<b>Profanity</b> {category_score_data['profanity']} / {risk_score_data['profanity']}"
    toxicity = f"<b>Toxicity</b> {category_score_data['toxicity']} / {risk_score_data['toxicity']}"
    severe_toxicity = f"<b>Severe Toxicity</b> {category_score_data['severe_toxicity']} / {risk_score_data['severe_toxicity']}"
    insult = f"<b>Insult</b> {category_score_data['insult']} / {risk_score_data['insult']}"
    identity_attack = f"<b>Identity Attack</b> {category_score_data['identity_attack']} / {risk_score_data['identity_attack']}"
    
      
    
    table_data = {
        'Data': [data_string],
        'Profanity': [profanity],
        'Toxicity': [toxicity],
        'Severe Toxicity': [severe_toxicity],
        'Insult' : [insult],
        'Identity Attack': [identity_attack],
        # ... add other metrics here, following the same pattern
    }
    
    df = pd.DataFrame(table_data)
    html_table = df.to_html(classes='table table-striped', escape=False, index=False)  # escape=False to render HTML tags
    
    # Add some styling to the HTML table
    html_table = f"""
    <style>
        .table-container {{
            width: 100%;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 1rem;
        }}
        .table {{
            width: 100%;
            margin-bottom: 1rem;
            color: #212529;
            border-collapse: collapse;
        }}
        .table-striped tbody tr:nth-of-type(odd) {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
    </style>
    <div class="table-container">
        {html_table}
    </div>
    """
    
    return {"table": html_table}

