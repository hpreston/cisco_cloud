'''
    Python module of different functions for manipulating ICF Director
    via the API.
'''

__author__ = 'hapresto'

# import standard variables and configuration info
from local_config import icfdserver, icfd_key, url, getstring, parameter_lead, headers
from cloud_library import dict_filter, list_search
headers["X-Cloupia-Request-Key"] = icfd_key

import requests
import json

def icfcloud_list(key_filter = [], result_filter = {}):
    '''
    Query ICF Director for a list of all icfClouds configured
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''

    apioperation = "Intercloud:userAPIGetAllicfClouds"
    getstring = "formatType=json&opName=%s"
    u = url % (icfdserver) + getstring % (apioperation)

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def workflow_inputs(workflow):
    '''
    Query ICF Director for the inputs for a workflow
    :param workflow: The workflow name to lookup inputs for
    :return:
    '''
    apioperation = "userAPIGetWorkflowInputs"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + workflow + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j['serviceResult']['details']

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
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + param0 + '",' + \
    'param1:{"list":' + json.dumps(param1) + '}' + \
    ',param2:' + param2 + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def icfcloud_startstop(icfCloudId):
    '''
    Create a Service Request to Start or Stop the icfCloud
    :param icfCloudId: The icfCloud ID to start or stop
    :return:
    '''
    param0 = "InterCloud Start Stop IcLink"
    icfCloud_input = {"Cloud Setup Id":icfCloudId}

    # Get the workflow inputs
    wf_inputs = workflow_inputs(param0)

    param1 = [{"name": i['label'], "value":icfCloud_input[i['label']]} for i in wf_inputs]
    param2 = "-1"

    apioperation = "userAPISubmitWorkflowServiceRequest"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + param0 + '",' + \
    'param1:{"list":' + json.dumps(param1) + '}' + \
    ',param2:' + param2 + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def icfcloud_details(icfCloudId, key_filter = [], result_filter = {}):
    '''
    Return the details of the specified icfCloud
    :param icfCloudId:  The icfCloud ID to return status for
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "Intercloud:userAPIGeticfCloudSummary"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + icfCloudId + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def sr_details(srnumber):
    '''
    Return the details of the Service Request Specified - Workflow Based Only
    :param srnumber: The Service Request ID
    :return: JSON of the SR Status
    '''
    apioperation = "userAPIGetServiceRequestWorkFlow"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + srnumber + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j['serviceResult']

def vm_list(key_filter = [], result_filter = {}):
    '''
    Return a list of all VMs known by ICF Director
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetAllVMs"
    getstring = "formatType=json&opName=%s"
    u = url % (icfdserver) + getstring % (apioperation)

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def vm_details(vmid, key_filter = [], result_filter = {}):
    '''
    Return the known details of the specified VM
    :param vmid: The ICFD VMID for the Virtual Machine
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "Intercloud:userAPIGetVMSummary"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    if j['serviceError']:
        return j['serviceError']
    else:
        j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)
        search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
        return search_results

def vm_poweron(vmid):
    '''
    Power on the specified Cloud Virtual Machine
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "Intercloud:userAPIVmPowerOn"
    # apioperation = "userAPIVmPowerOff"
    # apioperation = "userAPIVmReboot"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def vm_poweroff(vmid):
    '''
    Power off the specified Cloud Virtual Machine
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "Intercloud:userAPIVmPowerOff"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def vm_reboot(vmid):
    '''
    Reboot the specified Cloud Virtual Machine
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "Intercloud:userAPIVmReboot"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def vm_terminate(vmid):
    '''
    Terminate the specified Cloud Virtual Machine
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "Intercloud:userAPIVmTerminate"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def catalog_list(group="Default Group", key_filter = [], result_filter = {}):
    '''
    Get a list of Catalog Options for a Group
    :param group:  The ICFD Group to Query on behalf of
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetCatalogsPerGroup"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + group + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def catalog_order(catalog, vdc, comment=""):
    '''
    Order a catalog item
    :param catalog: The catalog to order
    :param vdc: The VDC to provision in
    :param comment: The comment or note.
    :return:
    '''
    param0 = catalog
    param1 = vdc
    param2 = comment

    apioperation = "Intercloud:userAPIProvisionVM"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + param0 + '",' + \
    "param1:\"" + param1 + '",' + \
    "param2:\"" + param2 + '"}'

    # print u

    r = requests.get(u, headers=headers)
    # print r.text

    j = json.loads(r.text)

    # vms = sr_vms()

    return j

def sr_vms(srnumber):
    '''
    Return the VMs of the Service Request Specified
    :param srnumber: The Service Request ID
    :return: JSON of the SR Status
    '''
    apioperation = "userAPIGetVMsForServiceRequest"
    u = url % (icfdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + srnumber + '"' + '}'

    r = requests.get(u, headers=headers)
    j = json.loads(r.text)

    return j['serviceResult']['vms']

def vdc_list(group="", provider="", key_filter = [], result_filter = {}):
    '''
    Return a list of all VDCs for a group if provided
    :param group:  The ICFD Group to return VDCs for... default all groups
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetAllVDCs"
    getstring = "formatType=json&opName=%s"
    u = url % (icfdserver) + getstring % (apioperation)

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    all_vdcs = j['serviceResult']['rows']
    group_vdcs = []

    for vdc in all_vdcs:
        if (vdc['Group'] == group or group == ""):
            if (vdc['Cloud'] == provider or provider ==""):
                group_vdcs.append(vdc)

    group_vdcs = list_search(group_vdcs, result_filter)

    search_results = [dict_filter(r, key_filter) for r in group_vdcs]
    return search_results

