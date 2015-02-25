#! /usr/bin/env python

'''
    Command Line Utility to return the list the Workflows in UCS Director
'''


import requests
import json
from ucsd_library import workflow_list

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('-f', '--folder',                          # Name stored in namespace
                   metavar = 'The UCSD Orchestration Library Folder',            # Arguement name displayed to user
                   help = 'What UCSD Orchestration Folder to Query - defaults to all',
                   type = str,
                   default=""
                    )

    ns = p.parse_args()

    sr = workflow_list(ns.folder)

    pprint (sr)

