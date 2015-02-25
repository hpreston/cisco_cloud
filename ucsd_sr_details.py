#! /usr/bin/env python

'''
    Command Line Utility to return the status of a UCS Director Service Requests
'''


import requests
import json
from ucsd_library import sr_details

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('srnumber',                          # Name stored in namespace
                   metavar = 'Service Request Number',            # Arguement name displayed to user
                   help = 'The Service Request return details of.',
                   type = str
                    )

    ns = p.parse_args()

    sr = sr_details(ns.srnumber)

    pprint (sr)

