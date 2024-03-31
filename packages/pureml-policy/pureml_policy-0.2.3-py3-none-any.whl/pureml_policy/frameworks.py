from pureml.schema import BackendSchema, ContentTypeHeader
from typing import Any
from importlib import import_module
from rich import print
import requests
from pureml.cli.auth import get_auth_headers
from .grade import Grader
from collections import defaultdict
import numpy as np
from urllib.parse import urljoin



def get_framework_details(framework_name):
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
                policies = framework_data["policies"]
                return {policy['metric']: policy['threshold'] for policy in policies if policy['type'] == 'test'}
                #return {policy['name']: policy['threshold'] for policy in policies if policy['type'] == 'test'}
            except Exception as e:
                print(f"Expection: {e}")
                print(f"Exception: {response.json()}")
        else:
            print("[red]Could not fetch the framework details")
            return None
        
