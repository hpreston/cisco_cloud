#! /usr/bin/env python

'''
    Command Line Utility to execute a given Workflow
'''


import requests
import json
from ucsd_library import workflow_execute


if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('workflow',                          # Name stored in namespace
                   metavar = 'Workflow Name',            # Arguement name displayed to user
                   help = 'The workflow to return inputs.',
                   type = str
                    )
    p.add_argument('-i', '--inputs',                          # Name stored in namespace
                   metavar = 'Workflow Inputs',            # Arguement name displayed to user
                   help = 'A dictionary of workflow inputs with the input name as the Key.',
                   type = json.loads
                    )

    ns = p.parse_args()

    result = workflow_execute(ns.workflow, ns.inputs)

    pprint (result)

