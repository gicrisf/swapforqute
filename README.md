# SwapForQute

> Redirect and clean URLs in qutebrowser.

SwapForQute (from now just SFQ) is an userscript for qutebrowser that replaces your URLs with new ones following an easy to set configuration.

See, as an example, this JSON snippet:

```json
{
  "www.reddit.com": {
    "out": "old.reddit.com",
    "force_https": true,
    "clean_queries": true
  },
  "reddit.com": {
    "out": "old.reddit.com",
    "force_https": true,
    "clean_queries": true
  }
}
```

When you bounce on a `www.reddit.com` or `reddit.com` URL, the script automatically tells the browser to search for the corresponding `old.reddit.com` one. As you can see, you can force HTTPS and clean queries, so that all tracking garbage is wiped out in the process.

# Installation and usage
Copy the script under your userscript directory:

``` sh
git clone --depth 1 https://github.com/gicrisf/swapforqute ~/.config/qutebrowser/userscripts
```

Give it the permissions to work on your system:

``` sh
chmod +x ~/.config/qutebrowser/userscripts/swapforqute/main.py
```

Now, edit the configuration as you please:

``` sh
vi ~/.config/qutebrowser/userscripts/swapforqute/config.json
```

It's all ready! Now set the keybindings in qutebrowser in compliance with your needs.

## Why I wrote this
I avoid running javascript on my browser for a lot of reasons: security, minimizing CPU usage, minimizing tracking... But some sites, usually big ones, heavily relies on JS for rendering content. When possible, I wished I could stay on privacy-friendly and js-free alternative frontends. Classic examples are offered by old reddit frontend VS new reddit frontend, nitter VS twitter, invidious VS youtube. With this script, it's possible to easily achieve all those redirects and every other you happen to think of.

<!-- # How it works -->

## Alternative ways
Before writing this script, I stepped on another userscript that aims at a similar goal, which is [Qutebrowser URL Mutator](https://codeberg.org/mister_monster/qutebrowser-url-mutator); it's thought to be configured via regexes, just like [Firefox "Redirector" extension](https://github.com/einaregilsson/Redirector). If you're used to this kind of workflow or you simply find it attractive, I suggest you to take a look at it.
Mutator was of inspiration for SFQ, so thanks to the author for its work!

## Requirements
A Python 3.7 (or newer) installation is required to run the script. It depends on standard libraries only (os, json, urllib, argparse). Obviously, being this an userscript for qutebrowser, [Qutebrowser](https://github.com/qutebrowser/qutebrowser) is required too.

## License
[MIT](https://github.com/gicrisf/swapforqute/blob/main/LICENSE)
