#! /usr/bin/env python

'''
    Command Line Utility to rollback a UCS Director Service Requests
'''


import requests
import json
from ucsd_library import sr_rollback


if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('srnumber',                          # Name stored in namespace
                   metavar = 'Service Request Number',            # Arguement name displayed to user
                   help = 'The Service Request to be rolled back.',
                   type = str
                    )

    ns = p.parse_args()

    sr = sr_rollback(ns.srnumber)

    pprint (sr)

