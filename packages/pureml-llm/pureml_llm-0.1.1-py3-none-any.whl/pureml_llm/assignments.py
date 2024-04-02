from pureml.components import  get_org_id
from pureml.schema import BackendSchema, ContentTypeHeader
from rich import print
import requests
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
from urllib.parse import urljoin
import json





#This Function is used to Assign Framework to a Model

def assign_framework_to_model(framework_name,label_model,sensitive_data):
    backend_schema = BackendSchema()
    org_id = get_org_id()
    model, model_version = label_model.split(':')
    #stringified_data_list = [(json.dumps(inner_list)).replace('"',"'").replace(' ','') for inner_list in sensitive_data]
    #data_dict = {"features": stringified_data_list}
    #print(f"Line 62. sensitive_data: {sensitive_data}")
    data_dict = {'features': sensitive_data}
    #json_data = json.dumps(data_dict)
    json_data = data_dict
    #print(f"Line 63. json_Data: {json_data}")
    #url = ASSIGN_FRAMEWORK_TO_MODEL_API.format(org_id=org_id, framework_name=framework_name, model=model, model_version=model_version)
    #print(url)
    url = f"assignments?orgId={org_id}&frameworkName={framework_name}&modelName={model}&version={model_version}"
    url = urljoin(backend_schema.BASE_URL, url)
    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
    response = requests.post(url, headers=headers, json = json_data)
    print(response.status_code)
    if not response.ok:
            print("Could not assign the framework to model")
            return False
    else:
        print("Framework assigned to model")
        

# This Functions is used to make the data ready to send to Update the Assignments.

def process_data(json_data, assignment_data):
    transformed_data = {}
    assignment_key_to_uuid = {}
    for key, value in assignment_data.items():
        try:
            processed_key = json.dumps(json.loads(key))
        except Exception  as e:
            processed_key = key
    
        assignment_key_to_uuid[processed_key] = value
    #assignment_key_to_uuid = {json.dumps(json.loads(key)): value for key, value in assignment_data.items()}
    
    def construct_key_from_subset(subset):
        column_values = [col['value'] for col in subset['column']]
        try:
            return json.dumps(column_values)
        except Exception as e:
            print(f"Exception: {e}")
            column_values = str(column_values[0])
            return json.dumps(column_values)
        
    
    # common_uuid_for_complete_policies = assignment_key_to_uuid['["complete"]']
    
    common_uuid_for_complete_policies = assignment_key_to_uuid.get('')
    
    for policy in json_data['policies']['complete']:
        metrics_dict = {}
        #print(f"Line 94. Policy: {policy}")
        metric_name = policy['name']
        if metric_name not in metrics_dict:
            metrics_dict[metric_name] = {}
        
        metrics_dict[metric_name] = float(policy['value'])
        metric_uuid_complete  = common_uuid_for_complete_policies[metric_name]
        transformed_data[metric_uuid_complete] = metrics_dict

    
    for subset in json_data['policies']['subsets']:
        key = construct_key_from_subset(subset)
        if key.startswith('[') and key.endswith(']'):
            if key in assignment_key_to_uuid:
                key_uuid = assignment_key_to_uuid[key]
            else:
                key_uuid = assignment_key_to_uuid[key[2]]
        else:
            pass
            #print(f"Key: {key}")
            #print(f"type of Key: {type(key)}")
        #metrics_dict = {}
        for policy in subset['policy']:
            metrics_dict = {}
            metric_name = policy['name']
            if metric_name not in metrics_dict:
                metrics_dict[metric_name] = {}
            metrics_dict[metric_name] = float(policy['value'])
            metric_uuid_subset = key_uuid[metric_name]
            transformed_data[metric_uuid_subset] = metrics_dict
    
    return transformed_data




# This Function is Used to Transfer Data to Update the Assignments

def transform_data_to_assignment_update_api(your_data,label_model):
    api_data_list = []
    model, model_version = label_model.split(':')
    for uuid, metrics in your_data.items():
        for metric_name, metric_value in metrics.items():
            api_data_list.append({
                "assignment_uuid": uuid,
                "metric": metric_name,
                "score": str(float(metric_value))  # Ensure the score is a float
            })

    api_payload = {"eval_json": api_data_list}

    data_sending = json.dumps(api_payload)
    #print(f"Data to send to API. Line 148: {data_sending}")
    url = f"assignments/update?orgId={get_org_id()}&modelName={model}&version={model_version}"
    backend_schema = BackendSchema()
    url = urljoin(backend_schema.BASE_URL, url)
    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
    response = requests.post(url, headers=headers, data=data_sending)
    print(response.status_code)
    if not response.ok:
        print("Could not update the assignments")
        return False
    else:
        print("Updated the assignments")
        return True



def update_assignments(data,label_model,framework_name):
    model,model_version = label_model.split(':')
    #data = json.stringify(data)
    payload  = {"eval_json": data}
    try:
        data_sending = json.dumps(payload)
        #data_sending = payload
        #with open('data.json', 'w') as f:
        #    f.write(data_sending)
        #data_sending = json_output(payload)
        #data_sending = json.dumps(json.dumps(payload))
        #print(f"Data to send to API. Line 182: {data_sending}")
        #url = f"evaluation_scores?orgId={get_org_id()}&modelName={model}&version={model_version}"
        #url = f"assignments/update?orgId={get_org_id()}&modelName={model}&version={model_version}&frameworkName={framework_name}"
        url = f"evaluation_scores?orgId={get_org_id()}&modelName={model}&version={model_version}"
        backend_schema = BackendSchema()
        url = urljoin(backend_schema.BASE_URL, url)
        headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
        response = requests.post(url, headers=headers, data=data_sending)
        print(response.status_code)
        if not response.ok:
            #print(response.message)
            error_message = response.json().get('message')
            print(response.json())
            print(f"Error Message: {error_message}")
            print("Could not update the assignments")
            return False
        else:
            print("Updated the assignments")
            return True
    except Exception as e:
        print(f"Exception: {e}")
    

def json_output(original_json):
    eval_json_string = original_json['eval_json']

    eval_json_string = eval_json_string[2:-2]

    eval_json_string = eval_json_string.replace('\\"', '"')

    eval_json_dict = json.loads(eval_json_string)

    eval_json_string_updated = json.dumps(eval_json_dict)

    original_json['eval_json'] = eval_json_string_updated

    final_json_string = json.dumps(original_json)

    return final_json_string