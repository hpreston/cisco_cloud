# Cisco Intercloud Fabric Scripts

This repository will provide python interfaces for manipulating and working with
Cisco's Cloud Software Stack including UCS Director and Intercloud Fabric Director.
(with others to come over time)

## Author Information

**Author** Hank Preston

**Contact Info** hapresto@cisco.com


## Usage

There are two main python modules that contain different functions for each product:

 * ucsd_library.py contains functions for working with UCS Director
 * icfd_library.py contains functions for working with ICF Director

Before using either the python functions or the CLI options, you must update/create
local_config.py with relant server_addresses and authkeys for your environment.

Other than the _library files, the others should all function as CLI scripts.
Run each with "-h" to get details on their use.  For example:

```bash
./ucsd_workflow_execute.py "Add VLAN to Data Center" -i '{"VLAN-ID":"1001", "VLAN Name":"NewVLAN"}'
``` 

Will create a Service Request to execute a workflow called "Add VLAN to Data Center"
with inputs of  ``` '{"VLAN-ID":"1001", "VLAN Name":"NewVLAN"}' ```

This repository is a living holding pen I use for labs and demos.  Check back often for updates.

****************************************************************************************************
Legal Disclaimer... 
The samples and code provided here is provided without warranty from myself or Cisco Systems.  
It is simply provided as an example of working with the APIs included in the referenced products, 
and was created by the author and is not an official extension of the software from Cisco.  
****************************************************************************************************
