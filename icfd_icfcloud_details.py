#! /usr/bin/env python

'''
    Command Line Utility to return a details for the selected IcfCloud
'''


import requests
import json
from icfd_library import icfcloud_details

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('icfCloudId',                          # Name stored in namespace
                   metavar = 'icfCloudId ID',            # Arguement name displayed to user
                   help = 'The ICFD IcfCloud ID to return details for.',
                   type = str
                    )

    ns = p.parse_args()

    result = icfcloud_details(ns.icfCloudId)

    pprint (result)

