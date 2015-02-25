'''
    Site specific configuration details for an implementation.
    Used to store server info, authentication keys, base urls, etc

    Update with your relevant information before running CLI scripts OR using the xxxd_library.py modules
'''

__author__ = 'hapresto'

# UCS Director Access Info  -  Update for your install
ucsdserver = "ucsd.local.intra"
ucsd_key = "XXXXXX"

# ICF Director Access Info  -  Update for your Install
icfdserver = "icfd.local.intra"
icfd_key = "XXXXXXXX"

# This information should stay the same for all users
url = "http://%s/app/api/rest?"
getstring = "formatType=json&opName=%s"
parameter_lead = "&opData="
headers = {"X-Cloupia-Request-Key":" "}

