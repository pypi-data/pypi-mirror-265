from pureml.components import dataset, get_org_id
from pureml.schema import BackendSchema, ContentTypeHeader
from typing import Any
from rich import print
import requests
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
import matplotlib.pyplot as plt
from urllib.parse import urljoin
import json
from .utils.routes import ASSIGN_FRAMEWORK_TO_MODEL_API
import numpy as np
from urllib.parse import urljoin, quote
from pureml.utils.logger import get_logger

logger = get_logger(name = 'pureml_policy.assignments.py')

# This Function is used to get Assignments from PureML Backend

def get_assignments(framework_name,label_model):
    backend_schema = BackendSchema()
    org_id = get_org_id()
    model, model_version = label_model.split(':')
    url = f"assignments?orgId={org_id}&frameworkName={framework_name}&modelName={model}&version={model_version}"
    url = urljoin(backend_schema.BASE_URL, url)
    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
    response = requests.get(url, headers=headers)
    if not response.ok:
            print("Could not fetch the assignments")
            return False
    else:
        print("Fetched the assignments")

    assignment_json = {}
    for i in range(len(response.json()['data'])):
        subsets = response.json()['data'][i]['subset']
        uuid = response.json()['data'][i]['uuid']
        metric_name  = response.json()['data'][i]['policy']['name']
        metric_uuid  = response.json()['data'][i]['uuid']
        if subsets not in assignment_json:
            assignment_json[subsets] = {} 
        assignment_json[subsets][metric_name] = metric_uuid

    #print(f"Json After Formatting.\nAssignments line 47: {assignment_json}")
    return assignment_json



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
        




def update_assignments(data,label_model):
    model,model_version = label_model.split(':')
    payload  = {"eval_json": data}
    try:
        data_sending = json.dumps(payload)
        #print(f"Data to send to API. Line 182: {data_sending}")
        encoded_model = quote(model)
        encoded_model_version = quote(model_version)
        org_id = quote(get_org_id())
        url = f"evaluation_scores?orgId={org_id}&modelName={encoded_model}&version={encoded_model_version}"
        #url = f"assignments/update?orgId={get_org_id()}&modelName={model}&version={model_version}&frameworkName={framework_name}"
        backend_schema = BackendSchema()
        url = urljoin(backend_schema.BASE_URL, url)
        #print(f"URL: {url}")
        logger.info(f"Payload for updating assignments: {data_sending}")
        logger.info(f"URL for sending to assignments to Backend: {url}")
        headers = get_auth_headers(content_type=ContentTypeHeader.ALL)
        response = requests.post(url, headers=headers, data=data_sending)
        print(f"Assignment Status Code: {response.status_code}")
        logger.info(f"Status code for updating assignments: {response.status_code}")
        if not response.ok:
            #print(response.raw)
            #print(response.json())
            error_message = response.json().get('message')
            logger.error(f"Could not update the assignments. Status Code: {response.status_code} & Error Message: {error_message}")
            print("Could not update the assignments")
            return False
        else:
            logger.info("Updated the assignments")
            print("Updated the assignments")
            return True
    except Exception as e:
        logger.error(f"Exception while updating assignments: {e}")
        print(f"Exception: {e}")
    