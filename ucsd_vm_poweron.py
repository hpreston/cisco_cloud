#! /usr/bin/env python

'''
    Command Line Utility to power on the selected VM
'''


import requests
import json
from ucsd_library import vm_poweron

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('vmid',                          # Name stored in namespace
                   metavar = 'Virtual Machine ID',            # Arguement name displayed to user
                   help = 'The ICFD vmid of the Cloud VM to power on.',
                   type = str
                    )

    ns = p.parse_args()

    result = vm_poweron(ns.vmid)

    pprint (result)

