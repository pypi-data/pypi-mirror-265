import inspect
import os
import requests
import subprocess
from typing import Any
import multiprocessing
from time import sleep

SAPHIRA_URL = os.getenv('SAPHIRA_URL', 'https://prod.saphira.ai')

# TODO: Integrate this into Matlab
# This registers as a daemon that will re-run the parent program
# TODO: Move daemon registration to service
def get_param(datasource: str, name: str, skip_threading=False, local_runtime=False) -> Any:
    # TODO: Call select_project first before selecting datasource 
    # TODO: Use datasource to route to appropriate multi-tenant (project)
    # Post to service
    url = f'{SAPHIRA_URL}/get_single_data/' + name
    req = {
        'check_key': name,
        # TODO: Include program name to allow automatic execution
        # 'consumingApplication': inspect.stack()[1].filename
    }
    consuming_application = inspect.stack()[-1].filename
    # resp = requests.post(url, json = req)
    resp = requests.get(url)
    print(f"{url} responded with status code {resp.status_code}, {resp.json()}")
    split_result = resp.json().get('value')
    # result = None
    result = split_result
    # if len(split_result) > 1:
    #     result = float(split_result[1])
    # else:
    #     raise Exception("bad response")
    
    if not skip_threading:
        if local_runtime:
            def loop():
                while True:
                    if get_param(datasource, name, skip_threading=True) != result:
                        subprocess.call(['python', consuming_application])
                    sleep(1)
            t = multiprocessing.Process(target=loop)
            t.start()
        else:
            # TODO: Perform proper dependency tracing to also upload any other linked files
            upload_url = f'{SAPHIRA_URL}/upload?project={datasource}&requirement={name}'
            stack = inspect.stack()
            files = {f'file{i}': open(stack[1 + i].filename, 'rb') for i in range(len(stack) - 1)}
            upload_resp = requests.post(upload_url, files=files)
            print(f"{upload_url} responded with status code {upload_resp.status_code}")

    return result
