'''
    Python module of different functions for manipulating UCS Director
    via the API.
'''

__author__ = 'hapresto'

# import standard variables and configuration info
from local_config import ucsdserver, ucsd_key, url, getstring, parameter_lead, headers
from cloud_library import dict_filter, list_search
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

def workflow_list(folder = "", key_filter = [], result_filter = {}):
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

    j['serviceResult'] = list_search(j['serviceResult'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']]
    return search_results

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


# Need to update notes and things below here
def vdc_list(group="", provider="", key_filter = [], result_filter = {}):
    '''
    Return a list of all VDCs for a group if provided
    :param group:  The UCSD Group to return VDCs for... default all groups
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetAllVDCs"
    getstring = "formatType=json&opName=%s"
    u = url % (ucsdserver) + getstring % (apioperation)

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

def vm_list(key_filter = [], result_filter = {}):
    '''
    Return a list of all VMs known by ICF Director
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetAllVMs"
    getstring = "formatType=json&opName=%s"
    u = url % (ucsdserver) + getstring % (apioperation)

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def vm_id(vmname):
    '''
    Find the VM ID given a VMname
    :param vmname:
    :return:
    '''
    return vm_list(result_filter={"VM_Name":vmname})[0]["VM_ID"]

def vm_details(vmid, key_filter = [], result_filter = {}):
    '''
    Return the known details of the specified VM
    :param vmid: The ICFD VMID for the Virtual Machine
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetVMSummary"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    if j['serviceError']:
        return j['serviceError']
    else:
        j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)
        search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
        return search_results

def vm_action(vmid, action, comments = ""):
    '''
    Power on the specified Cloud Virtual Machine
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "userAPIExecuteVMAction"
    # action = "powerOn"
    generic_actions = ["discardSaveState",
                       "pause",
                       "powerOff",
                       "powerOn",
                       "reboot",
                       "rebuildServer",
                       "repairVM",
                       "reset",
                       "resume",
                       "saveState",
                       "shutdownGuest",
                       "standby",
                       "suspend"
                       ]
    if action == "help": return generic_actions
    if not any(action == a for a in generic_actions): return "Action not valid"

    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + vmid + '",' + \
    'param1:"' + action + '"' + \
    ',param2:"' + comments + '"}'


    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def vm_getactions(vmid):
    '''
    Get Available Actions for a Given VM
    :param vmid:  The ICFD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "userAPIGetAvailableVMActions"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + vmid + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j['serviceResult']

def vm_terminate(vmid, comments = ""):
    '''
    Power on the specified Cloud Virtual Machine
    :param vmid:  The UCSD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''
    apioperation = "userAPIExecuteVMAction"
    action = "destroyVM"

    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + vmid + '",' + \
    'param1:"' + action + '"' + \
    ',param2:"' + comments + '"}'


    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    return j

def vm_poweron(vmid, comments = ""):
    '''
    Power on the specified Cloud Virtual Machine
    :param vmid:  The UCSD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''

    return vm_action(vmid, "powerOn", comments)

def vm_poweroff(vmid, comments = ""):
    '''
    Power on the specified Cloud Virtual Machine
    :param vmid:  The UCSD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''

    return vm_action(vmid, "shutdownGuest", comments)

def vm_reboot(vmid, comments = ""):
    '''
    Reboot the specified Cloud Virtual Machine
    :param vmid:  The UCSD VMID for the Cloud VM
    :param key_filter: A sub-list of keys from the returned data to filter for
    :return:
    '''

    return vm_action(vmid, "reboot", comments)


def catalog_list(group="", key_filter = [], result_filter = {}):
    '''
    Get a list of Catalog Options for a Group
    :param group:  The UCSD Group to Query on behalf of
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetCatalogsPerGroup"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
     "{param0:\"" + group + '"' + '}'

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)

    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def cloud_list(key_filter = [], result_filter = {}):
    '''
    Return a list of all clouds known by UCSD Director
    :param key_filter: A sub-list of keys from the returned data to filter for
    :param result_filter: A dictionary of key/value pairs to filter the result list down by (OR logic).
    :return:
    '''
    apioperation = "userAPIGetCloudsListReport"
    getstring = "formatType=json&opName=%s"
    u = url % (ucsdserver) + getstring % (apioperation)

    r = requests.get(u, headers=headers)

    j = json.loads(r.text)
    j['serviceResult']['rows'] = list_search(j['serviceResult']['rows'], result_filter)

    search_results = [dict_filter(r, key_filter) for r in j['serviceResult']['rows']]
    return search_results

def cloud_type(cloud):
    '''
    Returns the cloud type for the given cloud
    :param cloud:
    :return:
    '''
    cloud = cloud_list(result_filter={"Cloud":cloud})
    return cloud[0]["Cloud_Type"]

def catalog_cloud(catalog, group):
    '''
    Returns the cloud for the given catalog
    :param catalog:
    :param group:
    :return:
    '''
    c = catalog_list(group, result_filter={"Catalog_Name":catalog})
    return c[0]["Cloud"]

def catalog_type(catalog, group):
    '''
    Returns the catalog type for the given catalog
    :param catalog:
    :param group:
    :return:
    '''
    c = catalog_list(group, result_filter={"Catalog_Name":catalog})
    return c[0]["Catalog_Type"]

def catalog_order(catalog, vdc, group, comment="", vmname="", vcpus="0", vram="0", datastores="", vnics=""):
    '''
    Order a Standard Catalog Item
    :param catalog:
    :param vdc:
    :param group:
    :param comment:
    :param vmname:
    :param vcpus:
    :param vram:
    :param datastores:
    :param vnics:
    :return:
    '''
    # Get the catalog type, only STandard supported
    if catalog_type(catalog, group) != "Standard": return "Error: Only Standard Catalogs Supported.  " \
                                                          "Use 'workflow_execute' for Advanced Catalogs "

    # Get the type of cloud that the catalog is for
    catalog_cloud_type = cloud_type(catalog_cloud(catalog, group))
    # print catalog_cloud_type

    # Only support vCenter so far
    if catalog_cloud_type == "VMware":
        order = vmware_provision(catalog, vdc, comment, vmname, vcpus, vram, datastores, vnics)
        return order

    return "Invalid Request Provided"

def vmware_provision(catalog, vdc, comment="", vmname="", vcpus="0", vram="0", datastores="", vnics=""):
    '''
    Order a VMware based standard catalog
    :param catalog:
    :param vdc:
    :param comment:
    :param vmname:
    :param vcpus:
    :param vram:
    :param datastores:
    :param vnics:
    :return:
    '''
    param0 = catalog
    param1 = vdc
    param2 = vmname
    param3 = comment
    param4 = vcpus
    param5 = vram
    param6 = datastores
    param7 = vnics

    apioperation = "userAPIVMWareProvisionRequest"
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + param0 + '",' + \
    "param1:\"" + param1 + '",' + \
    "param2:\"" + param2 + '",' + \
    "param3:\"" + param3 + '",' + \
    "param4:" + param4 + ',' + \
    "param5:" + param5 + ',' + \
    "param6:\"" + param6 + '",' + \
    "param7:\"" + param7 + '"}'

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
    u = url % (ucsdserver) + getstring % (apioperation) + parameter_lead + \
    "{param0:\"" + srnumber + '"' + '}'

    r = requests.get(u, headers=headers)
    j = json.loads(r.text)

    return j['serviceResult']['vms']

