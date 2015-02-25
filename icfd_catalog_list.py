#! /usr/bin/env python

'''
    Command Line Utility to return a list of Catalog Options
'''


import requests
import json
from icfd_library import catalog_list

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('-g', '--group',                          # Name stored in namespace
                   metavar = 'ICFD End User Group',            # Arguement name displayed to user
                   help = 'The ICFD End User Group to Query for.  - Default to "Cloud Users',
                   type = str, default="Cloud Users@csc.richfield.cisco.com"
                    )

    ns = p.parse_args()

    result = catalog_list(ns.group)

    pprint (result)

