#! /usr/bin/env python

'''
    Command Line Utility to terminate the selected VM
'''


import requests
import json
from icfd_library import vm_terminate

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('vmid',                          # Name stored in namespace
                   metavar = 'Virtual Machine ID',            # Arguement name displayed to user
                   help = 'The ICFD vmid of the Cloud VM to terminate.',
                   type = str
                    )

    ns = p.parse_args()

    result = vm_terminate(ns.vmid)

    pprint (result)

