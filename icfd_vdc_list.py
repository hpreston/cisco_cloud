#! /usr/bin/env python

'''
    Command Line Utility to return a list of VDCs
'''


import requests
import json
from icfd_library import vdc_list

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('-g', '--group',                          # Name stored in namespace
                   metavar = 'ICFD End User Group',            # Arguement name displayed to user
                   help = 'The ICFD End User Group to Query for.  - Default to "Default Group"',
                   type = str, default="Default Group"
                    )
    p.add_argument('-p', '--provider',                          # Name stored in namespace
                   metavar = 'ICFD Provider Account',            # Arguement name displayed to user
                   help = 'The ICFD Provider Account.  - Default to All',
                   type = str, default=""
                    )

    ns = p.parse_args()

    result = vdc_list(ns.group, ns.provider)

    pprint (result)

