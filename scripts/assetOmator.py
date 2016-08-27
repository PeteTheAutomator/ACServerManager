#!/usr/bin/env python

import argparse
import os
from acserver_libs import AssetGatherer

acserver_builds = {
    '1d4e4ef8705a9471f6cb9a6c52512e45': '1249379',
    '54295196096b04ebbf658616284fed67': '1301003',
}


def argument_parser():
    parser = argparse.ArgumentParser(description='Assetto Corsa asset inspector - generates database fixtures')
    parser.add_argument('-s', '--steampath', help='path to Steam', required=False, default='c:\Steam')
    parser.add_argument('-o', '--outfile', default='assetto-assets.zip', help='Assetto Corsa asset output file archive')
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    args = argument_parser()

    while not os.path.isdir(args['steampath']):
        args['steampath'] = raw_input('Please enter the Steam installation folder?  (example "c:\Steam")\r\n')

    ag = AssetGatherer(args['steampath'])
    ag.validate_installation()
    ag.create()
