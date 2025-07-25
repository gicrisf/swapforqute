#!/usr/bin/env python3
import os
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(
    prog='swapforqute',
    description='Redirect and clean URLs in qutebrowser')

parser.add_argument('-u', '--url', help='URL that must be checked and maybe changed')
parser.add_argument('--cmd', help="Write Qutebrowser's command")

# Configuration rules - edit these as needed
RULES = {
    'example.com': {
        'force_https': True,
        'out': 'newexample.com',
        'clean_queries': True,
        'clean_fragments': True
    },
    'oldsite.org': {
        'force_https': True,
        'clean_queries': True
    }
}

def replace(url):
    out_url = urlparse(url)
    netloc = out_url.netloc
    
    # Apply rules if domain matches
    if netloc in RULES:
        instruct = RULES[netloc]
        
        # Force HTTPS
        if instruct.get('force_https', False):
            out_url = out_url._replace(scheme='https')
            
        # Replace domain
        if 'out' in instruct:
            out_url = out_url._replace(netloc=instruct['out'])
            
        # Clean queries
        if instruct.get('clean_queries', False):
            out_url = out_url._replace(query='')
            
        # Clean fragments
        if instruct.get('clean_fragments', False):
            out_url = out_url._replace(fragment='')
    
    return out_url.geturl()

if __name__ == "__main__":
    args = parser.parse_args()
    with open(os.environ["QUTE_FIFO"], "a") as o_fifo:
        o_fifo.write("{cmd} {url}\n".format(cmd=args.cmd, url=replace(args.url)))
