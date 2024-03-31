import pureml
from pureml.components import get_org_id
import requests
from pureml.cli.auth import get_auth_headers
from pureml.schema import BackendSchema, LogSchema, ConfigKeys, ContentTypeHeader
from .schema import framework_list
from urllib.parse import urljoin
import json


def get_framework_schema_details(framework_name='nyc144'):
    framework = framework_list[framework_name]

    task_type = framework['task_type']
    policies = framework['policies']
    sensitive_columns = framework['sensitive_columns']

    return task_type, policies, sensitive_columns


def get_framework_details(framework_name):

    backend_schema = BackendSchema()
    #backend_schema = BackendSchema().get_instance()

    url = "frameworks?frameworkName={}".format(
        framework_name
    )

    url = urljoin(backend_schema.BASE_URL, url)

    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)

    # data = json.dumps(data)

    response = requests.get(url, headers=headers)

    if response.ok:
        print(f"[bold green]UUID for framework: ",
              framework_name, " have been fetched!")
        framework_data = response.json()['data'][0]
        uuid = framework_data["uuid"]
        policies = framework_data["policies"]
        return uuid, policies

    else:
        print(f"[bold red]UUID for framework: ",
              framework_name, " have not been fetched!")

        return None, None


def post_framework_results(result_framework, model_name, model_version, framework_uuid):
    response = None
    if framework_uuid is not None:

        org_id = get_org_id()

        backend_schema = BackendSchema().get_instance()

        url = "reports?orgId={}&modelName={}&version={}".format(
            org_id, model_name, model_version
        )

        url = urljoin(backend_schema.BASE_URL, url)

        headers = get_auth_headers(content_type=ContentTypeHeader.ALL)

        result_framework = json.dumps(result_framework)
        data = {"data": result_framework, "framework_uuid": framework_uuid}

        data = json.dumps(data)

        response = requests.post(url, data=data, headers=headers)

        if response.ok:
            print(f"[bold green]framework results have been registered!")

        else:
            print(f"[bold red]framework results  have not been registered!")

    return response


def evaluate_with_framework(framework_name='nyc144', label_model=None, label_dataset=None):

    task_type, policies, sensitive_columns = get_framework_schema_details(framework_name)
    framework_uuid, framework_policies = get_framework_details(framework_name)

    metric_values = pureml.eval(task_type=task_type,
                                label_model=label_model,
                                label_dataset=label_dataset,
                                metrics=policies)   
        
    model_name, model_version = label_model.split(":")
    dataset_name, dataset_version = label_model.split(":")
    result_framework = {
        "framework_details": {
            "name": framework_name
        },
        "model_details": {
            "name": model_name,
            "version": model_version
        },
        "dataset_details": {
            "name": dataset_name,
            "version": dataset_version
        },
        "sensitive_columns": sensitive_columns,
        "policies": metric_values,
        "ethical_considerations": None,
        "Caveats_and_recommendations": None
    }

    response = post_framework_results(result_framework=result_framework,
                                   model_name=model_name,
                                   model_version=model_version,
                                   framework_uuid=framework_uuid)

    return result_framework, response
