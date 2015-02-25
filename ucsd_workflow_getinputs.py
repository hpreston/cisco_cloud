#! /usr/bin/env python

'''
    Command Line Utility to return the inputs for a given Workflow
'''


import requests
import json
from ucsd_library import workflow_inputs


if __name__ == '__main__':
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('workflow',                          # Name stored in namespace
                   metavar = 'Workflow Name',            # Arguement name displayed to user
                   help = 'The workflow to return inputs.',
                   type = str
                    )

    ns = p.parse_args()

    result = workflow_inputs(ns.workflow)

    pprint (result)

