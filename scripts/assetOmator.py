#!/usr/bin/env python

import argparse
import os
from acserver_libs import AssetGatherer

acserver_builds = {
    '1d4e4ef8705a9471f6cb9a6c52512e45': '1249379',
}


def argument_parser():
    parser = argparse.ArgumentParser(description='Assetto Corsa asset inspector - generates database fixtures')
    parser.add_argument('-s', '--steampath', help='path to Steam', required=False, default='c:\Steam')
    parser.add_argument('-o', '--outfile', default='assetto-assets.zip', help='Assetto Corsa asset output file archive')
    parser.add_argument('-i', '--ignore', help='ignore acserver md5 check - USE AT YOUR OWN RISK', action='store_true')
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    args = argument_parser()

    while not os.path.isdir(args['steampath']):
        args['steampath'] = raw_input('Please tell the the path to Steam?  (example "c:\Steam")\r\n')

    ag = AssetGatherer(args['steampath'])
    ag.validate_installation()

    if not args['ignore']:
        if not ag.validate_acserver_binary(acserver_builds):
            print 'The checksum of the Assetto Corsa Dedicated Server binary does not match what was expected; known working build IDs are: '
            for k in acserver_builds.keys():
                print acserver_builds[k]
            print 'The version you have installed may still work; you can try by adding the "--ignore" flag, but do so at your own risk.'

    ag.create()
