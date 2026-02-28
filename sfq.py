#!/usr/bin/env python3
import os
import argparse
import json
import re
from urllib.parse import urlparse

parser = argparse.ArgumentParser(
    prog='swapforqute',
    description='Redirect and clean URLs in qutebrowser')

parser.add_argument('-u', '--url', help='URL that must be checked and maybe changed')
parser.add_argument('--cmd', help="Write Qutebrowser's command")
parser.add_argument('-c', '--config', help='Path to JSON configuration file (extends built-in rules)')

# Configuration rules - edit these as needed
RULES = {
    # Exact-domain example with all transformations enabled.
    # "http://example.com/page?utm=1#top" -> "https://mirror-example.com/page"
    'example.com': {
        'force_https': True,
        'out': 'mirror-example.com',
        'clean_queries': True,
        'clean_fragments': True
    },
    # Exact-domain example without domain replacement.
    # "http://example.com/page?x=1#anchor" -> "https://example.com/page#anchor"
    'example.org': {
        'force_https': True,
        'clean_queries': True
    },
    # Simple wildcard example
    # "http://alpha.example.com/path?utm=1"
    # -> "https://alpha.mirror-example.com/path"
    '*.example.invalid': {
        'out': '$1.mirror-example.invalid',
        'force_https': True,
        'clean_queries': True
    },
    # Multiple wildcards example
    # "http://alpha.beta.example.com/path?utm=1"
    # -> "https://beta-alpha.mirror-example.com/path"
    '*.*.example.com': {
        'out': '$2-$1.mirror-example.com',
        'force_https': True,
        'clean_queries': True
    }
}

def load_config(config_path):
    """Load JSON configuration and extend RULES dictionary."""
    global RULES
    if 'RULES' not in globals():
        RULES = {}
    if config_path:
        config_path = os.path.expanduser(config_path)
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            json_rules = json.load(f)
            RULES.update(json_rules)

def replace(url):
    # Handle URLs without scheme (e.g., "reddit.com")
    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'https://' + url

    out_url = urlparse(url)
    host = out_url.hostname.lower() if out_url.hostname else out_url.netloc.lower()
    instruct = None
    star_parts = []

    # Prefer exact domain matches first to preserve existing behavior.
    if host in RULES:
        instruct = RULES[host]
    else:
        # Fall back to '*' wildcard patterns, most specific (most dots) first.
        wildcard_patterns = sorted(
            ((p, r) for p, r in RULES.items() if '*' in p.lower()),
            key=lambda pr: pr[0].count('.'),
            reverse=True
        )
        for pattern, candidate in wildcard_patterns:
            pattern_l = pattern.lower()
            # '*' matches any characters including '.', so *.example.com
            # matches both sub.example.com and a.b.sub.example.com.
            capture_re = re.escape(pattern_l).replace(r'\*', '(.*?)')
            match = re.fullmatch(capture_re, host)
            if not match:
                continue

            instruct = candidate
            star_parts = list(match.groups())
            break

    # Apply rules if domain matches
    if instruct:
        # Force HTTPS
        if instruct.get('force_https', False):
            out_url = out_url._replace(scheme='https')

        # Replace domain. Any port in the original URL is intentionally dropped:
        # it belongs to the source server, not the target. To keep a port,
        # include it explicitly in 'out' (e.g. "mirror.example.com:8080").
        if 'out' in instruct:
            target = instruct['out']
            for idx, value in enumerate(star_parts, start=1):
                target = target.replace('$' + str(idx), value)
            out_url = out_url._replace(netloc=target)

        # Clean queries
        if instruct.get('clean_queries', False):
            out_url = out_url._replace(query='')

        # Clean fragments
        if instruct.get('clean_fragments', False):
            out_url = out_url._replace(fragment='')

    return out_url.geturl()

if __name__ == "__main__":
    args = parser.parse_args()

    # Load JSON config if provided (extends built-in RULES)
    load_config(args.config)

    with open(os.environ["QUTE_FIFO"], "a") as o_fifo:
        o_fifo.write("{cmd} {url}\n".format(cmd=args.cmd, url=replace(args.url)))
