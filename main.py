#!/usr/bin/env python3

from urllib.parse import urlparse
import argparse
import os
import json

parser = argparse.ArgumentParser(
                    prog = 'swapforqute',
                    description = 'Redirect and clean URLs in qutebrowser',
                    epilog = '...')

parser.add_argument('-u', '--url', help='URL that must be checked and maybe changed')
parser.add_argument('-c', '--conf', help='Path of the JSON configuration')

def replace(url, conf):
    parsed = urlparse(url)

    with open(conf, "r") as read_file:
        conf = json.load(read_file)

    out_url = parsed

    for hypoth, instruct in conf.items():
        # Scheme
        if 'force_https' in instruct:
            if instruct['force_https']:
                out_url = parsed._replace(scheme='https')

        # Netloc
        if 'out' in instruct:
            out_url = parsed._replace(netloc=instruct['out'])

        # Queries
        if 'clean_queries' in instruct:
            if instruct['clean_queries']:
                out_url = parsed._replace(query='')

        # Frags
        if 'clean_fragments' in instruct:
            if instruct['clean_fragments']:
                out_url = parsed._replace(fragment='')

    return(out_url.geturl())

if __name__ == "__main__":
    args = parser.parse_args()
    with open(os.environ["QUTE_FIFO"], "a") as o_fifo:
        o_fifo.write("open -t " + replace(args.url, args.conf))
