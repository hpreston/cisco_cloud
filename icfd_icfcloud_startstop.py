#! /usr/bin/env python

'''
    Command Line Utility to Start or Stop an icfCloud
'''


import requests
import json
from icfd_library import icfcloud_startstop

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('icfCloudId',                          # Name stored in namespace
                   metavar = 'icfCloud ID',            # Arguement name displayed to user
                   help = 'The icfCloud ID to Start or Stop.',
                   type = str
                    )

    ns = p.parse_args()

    result = icfcloud_startstop(ns.icfCloudId)

    pprint (result)

