#! /usr/bin/env python

'''
    Command Line Utility to order a Catalog option
'''


import requests
import json
from icfd_library import catalog_order

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('catalog',                          # Name stored in namespace
                   metavar = 'ICFD Catalog',            # Arguement name displayed to user
                   help = 'The ICFD Catalog to order',
                   type = str
                    )
    p.add_argument('-v', '--vdc',                          # Name stored in namespace
                   metavar = 'ICFD VDC',            # Arguement name displayed to user
                   help = 'The ICFD VDC to place the cVM in',
                   type = str
                    )
    p.add_argument('-c', '--comment',                          # Name stored in namespace
                   metavar = 'ICFD Comment',            # Arguement name displayed to user
                   help = 'The comment to record - default blank',
                   type = str, default=""
                    )

    ns = p.parse_args()

    result = catalog_order(ns.catalog, ns.vdc, ns.comment)

    pprint (result)

