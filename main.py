#!/usr/bin/env python3
#
import os
import json
import argparse
from urllib.parse import urlparse
from os.path import expanduser

parser = argparse.ArgumentParser(
                    prog = 'swapforqute',
                    description = 'Redirect and clean URLs in qutebrowser',
                    epilog = '...')

parser.add_argument('-u', '--url', help='URL that must be checked and maybe changed')
parser.add_argument('--cmd', help="Write Qutebrowser's command")
parser.add_argument('-c', '--conf', help='Path of the JSON configuration')

def replace(url, conf):
    out_url = urlparse(url)

    # Read JSON configuration
    with open(expanduser(conf), "r") as f:
        conf = json.load(f)

    # Replace URL components
    for nl_hypoth, instruct in conf.items():
        if out_url.netloc == nl_hypoth:
            # Replace http scheme
            if 'force_https' in instruct:
                if instruct['force_https']:
                    out_url = out_url._replace(scheme='https')

            # Replace netloc
            if 'out' in instruct:
                out_url = out_url._replace(netloc=instruct['out'])

            # Delete queries
            if 'clean_queries' in instruct:
                if instruct['clean_queries']:
                    out_url = out_url._replace(query='')

            # Delete frags
            if 'clean_fragments' in instruct:
                if instruct['clean_fragments']:
                    out_url = out_url._replace(fragment='')

    return(out_url.geturl())

if __name__ == "__main__":
    args = parser.parse_args()
    with open(os.environ["QUTE_FIFO"], "a") as o_fifo:
        o_fifo.write("{cmd} {url}".format(cmd=args.cmd, url=replace(args.url, args.conf)))
