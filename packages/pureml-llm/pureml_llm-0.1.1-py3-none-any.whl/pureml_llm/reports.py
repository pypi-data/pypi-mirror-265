from pureml.components import  get_org_id
from pureml.schema import BackendSchema, ContentTypeHeader
from rich import print
import requests
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
from urllib.parse import urljoin




def get_reports(label_model,framework_name):
    backend_schema = BackendSchema()
    model,model_version = label_model.split(':')
    url = f"reports?orgId={get_org_id()}&modelName={model}&version={model_version}"
    url = urljoin(backend_schema.BASE_URL, url)
    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
    response = requests.get(url,headers=headers)
    for i in range(len(response.json()['data'])):
        if (response.json()['data'][i]['framework']['name'] == framework_name):
            result_url = response.json()['data'][i]['pdf_public_url']
    #result_url = response.json()['data'][0]['pdf_public_url']
    print(f"Use this URL to view Report: {result_url}")
    if response.ok:
        print("Reports Fetched")
        return response.json()
    else:
        print("Reports Not Fetched")
        return None

