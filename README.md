# SwapForQute

> Redirect and clean URLs in qutebrowser.

SwapForQute (or just SFQ) is an userscript for qutebrowser that replaces your URLs with new ones following an easy to set configuration.

```mermaid
graph TD
      Q[Qutebrowser] --> OLD["OLD URL:<br/>reddit.com/.../?utm_source=..."]
      OLD --> U[SFQ userscript]
      U --> NEW["NEW URL:<br/>old.reddit.com/..."]
      NEW --> Q

      classDef oldStyle fill:#ffcccc,stroke:#ff0000,color:#000
      classDef newStyle fill:#ccffcc,stroke:#00ff00,color:#000

      class OLD oldStyle
      class NEW newStyle
```

The diagram up here shows, as an example, what would happen with this configuration in the RULES dictionary:

```python
RULES = {
    'www.reddit.com': {
        'out': 'old.reddit.com',
        'force_https': True,
        'clean_queries': True
    },
    'reddit.com': {
        'out': 'old.reddit.com',
        'force_https': True,
        'clean_queries': True
    }
}
```

When you bounce on a `www.reddit.com` or `reddit.com` URL, the script automatically tells the browser to search for the corresponding `old.reddit.com` one. As you can see, you can force HTTPS and clean queries, so that all tracking garbage is wiped out in the process.
Therefore, something like "https://www.reddit.com/r/emacs/comments/yubhff/zwitterionic_digressions_get_user_inputs_in_emacs/?utm_source=share&utm_medium=web2x&context=3" magically become "https://old.reddit.com/r/emacs/comments/yubhff/zwitterionic_digressions_get_user_inputs_in_emacs".

## Quickstart

### Linux / macOS

**1. Install the script:**

``` sh
curl -fsSL https://raw.githubusercontent.com/gicrisf/swapforqute/main/install.sh | bash
```

**2. Add to your qutebrowser `config.py`:**

``` python
sfq_script_path = "~/.config/qutebrowser/userscripts/sfq.py"
sfq_cmd = "--userscript {}".format(sfq_script_path)
c.aliases['sfq'] = "set-cmd-text -s :spawn {} --cmd 'open' -u ".format(sfq_cmd)
config.bind('o', ':sfq')  # Bind to your preferred key
```

**3. Customize rules in `~/.config/qutebrowser/userscripts/sfq.py`:**

Edit the `RULES` dictionary to add your own URL transformations. See [Configuration](#configuration) for details.

### Windows

**1. Install the script:**

``` powershell
irm https://raw.githubusercontent.com/gicrisf/swapforqute/main/install.ps1 | iex
```

**2. Add to your qutebrowser `config.py`:**

``` python
import os
# N.B. We need to call the batch wrapper on Windows!
# Don't worry, nothing else change, just watch out you don't copypaste from a linux configuration directly
sfq_script_path = os.path.join(os.getenv('APPDATA'), 'qutebrowser', 'userscripts', 'sfq.bat')
sfq_cmd = "--userscript {}".format(sfq_script_path)
c.aliases['sfq'] = "set-cmd-text -s :spawn {} --cmd 'open' -u ".format(sfq_cmd)
config.bind('o', ':sfq')  # Bind to your preferred key
```

**3. Customize rules in `%APPDATA%\qutebrowser\userscripts\sfq.py`:**

Edit the `RULES` dictionary to add your own URL transformations. See [Configuration](#configuration) for details.

## Manual Installation

If you prefer to install manually or want more control over the process:

### Linux / macOS

```sh
# Create the userscripts directory if it doesn't exist
mkdir -p ~/.config/qutebrowser/userscripts

# Download the latest release
curl -L -o ~/.config/qutebrowser/userscripts/sfq.py \
  https://github.com/gicrisf/swapforqute/releases/latest/download/sfq.py

# Make it executable
chmod +x ~/.config/qutebrowser/userscripts/sfq.py
```

### Windows

``` powershell
# Create the userscripts directory if it doesn't exist
$InstallDir = "$env:APPDATA\qutebrowser\userscripts"
New-Item -ItemType Directory -Force -Path $InstallDir

# Download the latest release
Invoke-WebRequest -Uri "https://github.com/gicrisf/swapforqute/releases/latest/download/sfq.py" `
  -OutFile "$InstallDir\sfq.py"

# Create batch wrapper (required for Windows)
$BatchContent = @"
@echo off
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%sfq.py" %*
"@
Set-Content -Path "$InstallDir\sfq.bat" -Value $BatchContent
```

### Setup aliases and keybindings

It's not feasible to write all the command's clutter everytime.
Better writing a simple alias like `:sfq` in `config.py`:

``` python
# Linux/macOS
sfq_script_path = "~/.config/qutebrowser/userscripts/sfq.py"

# Windows (use sfq.bat)
# import os
# sfq_script_path = os.path.join(os.getenv('APPDATA'), 'qutebrowser', 'userscripts', 'sfq.bat')

sfq_cmd = "--userscript {}".format(sfq_script_path)
c.aliases['sfq'] = "set-cmd-text -s :spawn {} --cmd 'open' -u ".format(sfq_cmd)
```

The obvious next step is setting up the keybindings:

``` python
config.bind('o', ':sfq')
```

## Configuration

SwapForQute supports two configuration approaches:

### 1. Built-in Rules (Easier)

Edit the `RULES` dictionary directly in `sfq.py` (lines 16-27). This is the simplest approach and requires no additional command-line arguments:

``` python
RULES = {
    'example.com': {
        'force_https': True,
        'out': 'newexample.com',
        'clean_queries': True,
        'clean_fragments': True
    }
}
```

### 2. JSON Configuration (Optional)

For users who prefer keeping configuration separate, you can create a JSON config file anywhere and use the `-c` flag to extend the built-in rules.

Create a JSON file with your custom rules:

``` json
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

When you provide a JSON config file, it **extends** (not replaces) the built-in rules. If a domain appears in both, the JSON rule takes precedence.

### Rule Options

For each domain, you can set:
- `out`: Replace the domain with this value
- `force_https`: Force HTTPS scheme (true/false)
- `clean_queries`: Delete all query parameters (true/false)
- `clean_fragments`: Delete URL fragments (true/false)

Every element is optional. You can choose to force https requests without touching the other components of the URL or cleaning the fragments without touching the queries.

### Using JSON Config with the `-c` Flag

``` python
# Build the command with JSON config (put config.json wherever you want)
sfq_script_path = "~/.config/qutebrowser/userscripts/sfq.py"
sfq_conf_path = "~/.config/qutebrowser/config.json"  # Or any path you prefer
sfq_cmd = "--userscript {} -c {}".format(sfq_script_path, sfq_conf_path)

# Assign the alias
c.aliases['sfq'] = "set-cmd-text -s :spawn {} --cmd 'open' -u ".format(sfq_cmd)

# Optional: bind to a key
config.bind('o', ':sfq')
```

Personally, I prefer leaving the default command for `o` key and assign `:sfq` to a special sequence, for `f` (hint links) and something else. [Check my qutebrowser literate configuration](https://github.com/gicrisf/qute-config) for a more extended explanation of command building, keybindings and other tricks.

Of course, you can be creative and came up with your own solutions: the script just process your input to give you an output, but it's up to you where and when to use it.

## Why I wrote this
I avoid running javascript on my browser for a lot of reasons: security, minimizing CPU usage, minimizing tracking... But some sites, usually big ones, heavily relies on JS for rendering content. When possible, I wished I could stay on privacy-friendly and js-free alternative frontends. Classic examples are offered by old reddit frontend VS new reddit frontend, nitter VS twitter, invidious VS youtube. With this script, it's possible to easily achieve all those redirects and every other you happen to think of.

## How it works

```mermaid
graph TD
      subgraph QB[Qutebrowser]
          CMD[SFQ command]
      end

      SCRIPT[SFQ userscript]
      RULES[RULES]
      FIFO[QUTE FIFO]

      CMD -->|old url| SCRIPT
      SCRIPT -.->|1.checks| RULES
      RULES -.->|2.applies| SCRIPT
      SCRIPT -->|3.new url| FIFO
      FIFO --> QB
```

## Alternative ways
Before writing this script, I stepped on another userscript that aims at a similar goal, which is [Qutebrowser URL Mutator](https://codeberg.org/mister_monster/qutebrowser-url-mutator); it's thought to be configured via regexes, just like [Firefox "Redirector" extension](https://github.com/einaregilsson/Redirector). If you're used to this kind of workflow or you simply find it attractive, I suggest you to take a look at it.
Mutator was of inspiration for SFQ, so thanks for that!

## Requirements
This userscript uses Python standard libraries only. Since it runs in [qutebrowser](https://github.com/qutebrowser/qutebrowser), which depends on Python, all requirements are automatically satisfied.

## Testing
The project includes a comprehensive test suite. Run tests with:
```bash
python -m unittest test_sfq
```

## Support
Why don't you help me keeping myself awake buying me a coffee?
I could use the extra time to add more features!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/V7V425BFU)

<a href="https://liberapay.com/gicrisf/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>

## License
[MIT](https://github.com/gicrisf/swapforqute/blob/main/LICENSE)
