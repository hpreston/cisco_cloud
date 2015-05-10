#! /usr/bin/env python

'''
    Command Line Utility to return a the VMs in a SR
'''


import requests
import json
from ucsd_library import sr_vms

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('sr',                          # Name stored in namespace
                   metavar = 'UCSD SR that ordered the VMs',            # Arguement name displayed to user
                   help = 'The Service Request to get VMs for.  ',
                   type = str
                    )

    ns = p.parse_args()

    result = sr_vms(ns.sr)

    pprint (result)

