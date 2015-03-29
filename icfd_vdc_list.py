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
                   help = 'The ICFD End User Group to Query for.  - Default to All Groups',
                   type = str, default=""
                    )
    p.add_argument('-p', '--provider',                          # Name stored in namespace
                   metavar = 'ICFD Provider Account',            # Arguement name displayed to user
                   help = 'The ICFD Provider Account.  - Default to All',
                   type = str, default=""
                    )
    p.add_argument('-f',                          # Name stored in namespace
                   metavar = 'A field to return',            # Arguement name displayed to user
                   help = 'Which detail fields to return.  Can be used multiple times.',
                   type = str, action="append", default = []
                    )
    p.add_argument('-k',
                   metavar = "The field to search.  ",
                   help = "Which detail field to search for.",
                   type = str
                   )
    p.add_argument('-v',
                   metavar = "The value to search for.  ",
                   help = "What value to search the detail field for.",
                   type = str
                   )
    ns = p.parse_args()
    if (ns.k and ns.v): rf = {ns.k:ns.v}
    else: rf = {}

    result = vdc_list(ns.group, ns.provider, key_filter=ns.f, result_filter = rf)

    pprint (result)

