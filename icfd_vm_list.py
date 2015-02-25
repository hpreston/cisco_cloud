#! /usr/bin/env python

'''
    Command Line Utility to return a list of all VMs
'''


import requests
import json
from icfd_library import vm_list

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()


    ns = p.parse_args()

    result = vm_list()

    pprint (result)

