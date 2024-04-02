from pureml.components import dataset, get_org_id
from pureml.schema import BackendSchema, ContentTypeHeader
from typing import Any
from importlib import import_module
from rich import print
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pureml_evaluate.evaluators.evaluator import eval as eval_fn
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
from .grade import Grader
from collections import defaultdict
import numpy as np
from urllib.parse import urljoin
import json
import pandas as pd





# This Function is used to Send Reports to PureML Backend

def send_reports(data,framework_name,label_model):
    model,model_version  = label_model.split(':')
    backend_schema = BackendSchema()
    url = f"frameworks/{framework_name}"
    url = urljoin(backend_schema.BASE_URL, url)
    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
    response = requests.get(url, headers=headers)
    if response.ok:
        print("[green]Succesfully fetched the framework details")
        try:
            framework_data = response.json()['data'][0]
            uuid = framework_data["uuid"]
        except Exception as e:
            print(f"Expection: {e}")
            print(f"Exception: {response.json()}")
    url = f"reports?orgId={get_org_id()}&modelName={model}&version={model_version}"
    url = urljoin(backend_schema.BASE_URL, url)
    try:
        data = json.dumps(data)
    except Exception as e:
        print(f"Exception: {e}")
        data = convert(data)
    data_to_send = {
        "data" : str(data),
        "framework_uuid" : str(uuid)
    }
    
    sending_data = json.dumps(data_to_send)
    response = requests.post(url,headers=headers,data = sending_data)
    if response.ok:
        print("Report Generated")
    





# This Function is to get Reports from PureML Backend

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


