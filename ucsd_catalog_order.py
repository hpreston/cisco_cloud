#! /usr/bin/env python

'''
    Command Line Utility to order a Catalog option
'''


import requests
import json
from ucsd_library import catalog_order

if __name__ == '__main__':

    import sys
    from pprint import pprint
    from argparse import ArgumentParser, FileType

    p = ArgumentParser()
    p.add_argument('catalog',                          # Name stored in namespace
                   metavar = 'UCSD Catalog',            # Arguement name displayed to user
                   help = 'The UCSD Catalog to order',
                   type = str
                    )
    p.add_argument('-v', '--vdc',                          # Name stored in namespace
                   metavar = 'UCSD VDC',            # Arguement name displayed to user
                   help = 'The UCSD VDC to place the cVM in',
                   type = str
                    )
    p.add_argument('-c', '--comment',                          # Name stored in namespace
                   metavar = 'UCSD Comment',            # Arguement name displayed to user
                   help = 'The comment to record - default blank',
                   type = str, default=""
                    )
    p.add_argument('-g', '--group',                          # Name stored in namespace
                   metavar = 'UCSD Group',            # Arguement name displayed to user
                   help = 'The group to order on behalf of',
                   type = str, default=""
                    )
    p.add_argument('-n', '--vmname',                          # Name stored in namespace
                   metavar = 'UCSD VMname',            # Arguement name displayed to user
                   help = 'The VM Name or prefix',
                   type = str, default=""
                    )
    p.add_argument('--vcpus',                          # Name stored in namespace
                   metavar = 'vCPU Count',            # Arguement name displayed to user
                   help = 'The number of vCPUs.  Only used if vDC allows',
                   type = str, default="0"
                    )
    p.add_argument('--vram',                          # Name stored in namespace
                   metavar = 'vRAM Count',            # Arguement name displayed to user
                   help = 'The amount of vRAM.  Only used if vDC allows',
                   type = str, default="0"
                    )
    p.add_argument('--datastores',                          # Name stored in namespace
                   metavar = 'Datastore details',            # Arguement name displayed to user
                   help = 'The datastore details.  Only used if vDC allows.',
                   type = str, default=""
                    )
    p.add_argument('--vnics',                          # Name stored in namespace
                   metavar = 'vNIC Details',            # Arguement name displayed to user
                   help = 'The details for vNICS.  Only used if vDC allows',
                   type = str, default=""
                    )

    ns = p.parse_args()

    result = catalog_order(ns.catalog, ns.vdc, ns.group, ns.comment, ns.vmname, ns.vcpus, ns.vram, ns.datastores, ns.vnics)

    pprint (result)

