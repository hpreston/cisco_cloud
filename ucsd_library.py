'''
    Python module of different functions for manipulating UCS Director
    via the API.
'''

__author__ = 'hapresto'

# import standard variables and configuration info
from local_config import ucsdserver, ucsd_key, url, getstring, parameter_lead, headers
headers["X-Cloupia-Request-Key"] = ucsd_key

import requests
import json

def workflow_inputs(workflow):
    '''
    Query UCS Director for the inputs for a workflow
    :param workflow: The workflow name to lookup inputs for
    :return:
    '''
    apioperation = "userAPIGetWorkflowInputs"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + workflow + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j['serviceResult']['details']

def workflow_list(folder = ""):
    '''
    Query UCS Director for the workflows for a folder
    :param folder: The UCSD Orchestration Folder to Query - defaults to all
    :return:
    '''
    apioperation = "userAPIGetWorkflows"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + folder + '"' + '}'

    r = requests.get(u, headers=headers)
    j = json.loads(r.text)

    return j['serviceResult']

def workflow_execute(workflow, inputs):
    '''
    Create a Service Request based on the specified Workflow and with Inputs.
    :param workflow:    The workflow name to execute
    :param inputs:      dict of inputs with Input Label as Key
    :return:            JSON of the Service Request Created
    '''
    param0 = workflow

    # Get the workflow inputs
    wf_inputs = workflow_inputs(workflow)

    param1 = [{"name": i['label'], "value":inputs[i['label']]} for i in wf_inputs]
    param2 = "-1"

    apioperation = "userAPISubmitWorkflowServiceRequest"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + param0 + '",' + \
    'param1:{"list":' + json.dumps(param1) + '}' + \
    ',param2:' + param2 + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def sr_rollback(srnumber):
    '''
    Rollback the Service Request Specified
    :param srnumber: The Service Request ID
    :return: JSON status of the request
    '''
    apioperation = "userAPIRollbackWorkflow"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + srnumber + '"' + '}'

    r = requests.get(u, headers=headers)

    return r.text

def sr_details(srnumber):
    '''
    Return the details of the Service Request Specified - Workflow Based Only
    :param srnumber: The Service Request ID
    :return: JSON of the SR Status
    '''
    # apioperation = "userAPIGetServiceRequestDetails"
    apioperation = "userAPIGetServiceRequestWorkFlow"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + srnumber + '"' + '}'

    r = requests.get(u, headers=headers)

    return r.text
