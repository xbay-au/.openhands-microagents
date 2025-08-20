#!/usr/bin/env python3
import threading
import base64
import getpass
import os
import sys
import subprocess
import json
import random
import time
from datetime import datetime

# Dependencies: requests, rich, tqdm
try:
    from tqdm import tqdm
except ImportError:
    print("Missing dependency 'tqdm'. Please run: pip install tqdm")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Missing dependency 'requests'. Please run: pip install requests")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("Missing dependency 'rich'. Please run: pip install rich")
    sys.exit(1)

console = Console()

# Optional User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
]


# Configuration
WORDLIST_DIR = os.environ.get('WORDLIST_DIR', '/workspace/wordlists')
HISTORY_FILE = os.environ.get('FFUF_HISTORY_FILE', os.path.expanduser('~/.ffuf_agent_history.json'))
FFUF_CMD = os.environ.get('FFUF_PATH', 'ffuf')

# Predefined wordlist URLs
# Expanded with Quick/Comprehensive profiles

WORDLIST_URLS = {
    "directory-list-2.3-medium.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt",
    "api-endpoints.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/api-endpoints.txt",
    "subdomains-top1mil-5000.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1mil-5000.txt",
    "file-extensions.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/file-extensions.txt",
    "path-traversal.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/raft-medium-words.txt",
    "origins.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Cors/origins.txt",
    "js-endpoints.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/js-endpoints.txt",
}

SCAN_TYPES = {
    "1": ("Directory & File Discovery", "directory-list-2.3-medium.txt"),
    "2": ("API Endpoint Discovery", "api-endpoints.txt"),
    "3": ("Subdomain Enumeration", "subdomains-top1mil-5000.txt"),
    "4": ("File Leak Detection", "file-extensions.txt"),
    "5": ("Virtual Host Discovery", "subdomains-top1mil-5000.txt"),
    "6": ("Path Traversal Fuzzing", "path-traversal.txt"),
    "7": ("CORS Misconfiguration Checks", "origins.txt"),
    "8": ("JavaScript Endpoint Discovery", "js-endpoints.txt"),
    "9": ("Custom Wordlist", None),
    "10": ("Recursive Scanning", "directory-list-2.3-medium.txt"),
}


# Scan profiles presets
PROFILES = {
    "1": ("None", {"threads": 50, "delay": 0, "autocal": False}),
    "2": ("Stealth", {"threads": 10, "delay": 200, "autocal": True}),
    "3": ("Balanced", {"threads": 40, "delay": 100, "autocal": True}),
    "4": ("Fast", {"threads": 100, "delay": 0, "autocal": False}),
}


def ensure_wordlist(name):
    """Ensure wordlist exists locally, or download it."""
    os.makedirs(WORDLIST_DIR, exist_ok=True)
    path = os.path.join(WORDLIST_DIR, name)
    if os.path.isfile(path):
        return path
    url = WORDLIST_URLS.get(name)
    if not url:
        console.print(f"No known URL for wordlist '{name}'. Please download manually.", style="red")
        sys.exit(1)
    console.print(f"Downloading wordlist [cyan]{name}[/cyan]...")
    resp = requests.get(url, stream=True)
    if resp.status_code != 200:
        console.print(f"Failed to download {name} (HTTP {resp.status_code}).", style="red")
        sys.exit(1)
    with open(path, 'wb') as f:
        total = int(resp.headers.get('content-length', 0))
        for chunk in tqdm(resp.iter_content(chunk_size=8192), total=(total//8192) or None, unit='chunk'):
            f.write(chunk)
    console.print(f"Saved to {path}")
    return path


def choose_scan_type():
    console.print("[bold]Select scan type:[/bold]")
    for k, v in SCAN_TYPES.items():
        console.print(f" {k}) {v[0]}")
    choice = console.input("Choice [1-10]: ").strip()
    if choice not in SCAN_TYPES:
        console.print("Invalid choice.", style="red")
        return choose_scan_type()
    return choice, SCAN_TYPES[choice]


def get_target_url(scan_key):
    stype, _ = SCAN_TYPES[scan_key]
    if scan_key == '3' or scan_key == '5':
        host = console.input("Base domain (e.g. example.com): ").strip()
        return f"http://FUZZ.{host}"
    else:
        url = console.input("Target URL (include http:// or https://, use FUZZ where appropriate): ").strip()
        if 'FUZZ' not in url:
            console.print("URL must contain 'FUZZ' placeholder.", style="red")
            return get_target_url(scan_key)
        return url


def input_generic(prompt, default=None):
    resp = console.input(f"{prompt}{' ['+default+']' if default else ''}: ").strip()
    if not resp and default is not None:
        return default
    return resp


def build_command(params):
    cmd = [FFUF_CMD]
    # Inject a random User-Agent header if none specified
    if not any(h.lower().startswith('user-agent') for h in params['headers']):
        ua = random.choice(USER_AGENTS)
        cmd += ['-H', f'User-Agent: {ua}']

    cmd += ['-w', params['wordlist']]
    cmd += ['-u', params['url']]
    cmd += ['-mc', params['status_codes']]
    cmd += ['-t', str(params['threads'])]
    if params['color']:
        cmd.append('-c')
    if params['autocal']: 
        cmd.append('-ac')
    for h in params['headers']:
        cmd += ['-H', h]
    if params['proxy']:
        cmd += ['-x', params['proxy']]
    if params['delay']:
        cmd += ['-delay', str(params['delay'])]
    if params['recursion']:
        cmd += ['-recursion', '-recursion-depth', str(params['depth'])]

        # Decoy requests
        if params.get('decoy'):
            cmd += ['-D', params['decoy']]
    # output JSON
    outfile = params['output']
    cmd += ['-of', 'json', '-o', outfile]
    return cmd


def run_ffuf(cmd):
    console.print(f"Running: [bold]{' '.join(cmd)}[/bold]")
    # Display live progress spinner while ffuf runs
    with console.status("[bold green]Scanning in progress...[/bold green]", spinner="dots"):
        result = subprocess.run(cmd)
    if result.returncode != 0:
        console.print(f"FFUF exited with code {result.returncode}", style="red")
    return result


def parse_results(outfile):
    try:
        data = json.load(open(outfile))
    except Exception as e:
        console.print(f"Failed to parse JSON output: {e}", style="red")
        return None
    # data is list of entries
    counts = {}
    for entry in data.get('results', data):
        code = str(entry.get('status', entry.get('status_code', ''))) 
        counts[code] = counts.get(code, 0) + 1
    table = Table(title="FFUF Results Summary")
    table.add_column("Status Code")
    table.add_column("Hits", justify="right")
    for code, cnt in sorted(counts.items()):
        table.add_row(code, str(cnt))
    console.print(table)
    return {'counts': counts, 'total': sum(counts.values())}


def update_history(entry):
    history = []
    if os.path.isfile(HISTORY_FILE):
        try:
            history = json.load(open(HISTORY_FILE))
        except:
            history = []
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)




def load_history():
    """Load scan history from disk."""
    if os.path.isfile(HISTORY_FILE):
        try:
            return json.load(open(HISTORY_FILE))
        except:
            return []
    return []


def show_history_menu():
    """Display past scans and allow re-run or deletion."""
    history = load_history()
    if not history:
        console.print("No scans in history.", style="yellow")
        return
    table = Table(title="Scan History")
    table.add_column("#", justify="right")
    table.add_column("Timestamp")
    table.add_column("Scan Type")
    table.add_column("Total Hits", justify="right")
    for idx, entry in enumerate(history, start=1):
        total = entry.get('summary', {}).get('total', 0)
        table.add_row(str(idx), entry.get('timestamp', ''), entry.get('scan_type', ''), str(total))
    console.print(table)
    choice = console.input("Select entry number to re-run, or 'd<nr>' to delete, blank to return: ").strip()
    if not choice:
        return
    # Deletion
    if choice.startswith('d'):
        try:
            num = int(choice[1:])
            if 1 <= num <= len(history):
                del history[num-1]
                with open(HISTORY_FILE, 'w') as f:
                    json.dump(history, f, indent=2)
                console.print(f"Deleted entry {num}.", style="green")
            else:
                console.print("Invalid entry number.", style="red")
        except ValueError:
            console.print("Invalid selection.", style="red")
        return
    # Re-run selection
    try:
        num = int(choice)
    except ValueError:
        console.print("Invalid selection.", style="red")
        return
    if not (1 <= num <= len(history)):
        console.print("Invalid entry number.", style="red")
        return
    entry = history[num-1]
    console.print(f"Re-running scan from {entry['timestamp']} ({entry['scan_type']})", style="cyan")
    params = entry['params']
    cmd = build_command(params)
    res = run_ffuf(cmd)
    summary = None
    if os.path.isfile(params['output']):
        summary = parse_results(params['output'])
    new_entry = {
        'timestamp': datetime.now().isoformat(),
        'scan_type': entry['scan_type'],
        'params': params,
        'summary': summary
    }
    update_history(new_entry)
    console.print("Re-run complete.", style="green")


def main():
    console.print("[bold green]FFUF Interactive Agent[/bold green]")
    # Top-level menu: new scan or history
    choice = console.input("Select: [bold]n[/bold] for new scan, [bold]h[/bold] for history [n]: ").strip().lower()
    if choice == 'h':
        show_history_menu()
        return

    scan_key, (stype, default_list) = choose_scan_type()
    # Determine wordlist
    if scan_key == '9':
        custom = console.input("Path to custom wordlist: ").strip()
        wordlist = custom
    else:
        wordlist_name = custom if scan_key=='9' else default_list
        wordlist = ensure_wordlist(wordlist_name)
        # Initialize headers list
    headers = []
    # Authentication
    auth_choice = console.input("Authentication (none/basic/bearer) [none]: ").strip().lower()
    if auth_choice == 'basic':
        username = console.input("Username: ").strip()

    # Scan profile selection
    console.print("[bold]Scan Profile Selection:[/bold]")
    for key, (pname, cfg) in PROFILES.items():
        console.print(f" {key}) {pname}")
    prof_choice = input_generic("Profile", default="3")
    name, cfg = PROFILES.get(prof_choice, PROFILES["3"])
    threads = cfg["threads"]
    delay = cfg["delay"]
    autocal = cfg["autocal"]
    console.print(f"Using profile [cyan]{name}[/cyan]: threads={threads}, delay={delay}, autocalibrate={autocal}")
    if input_generic("Customize profile settings? (y/n)", default="n").lower().startswith('y'):
        threads = int(input_generic("Threads", default=str(threads)))
        delay = int(input_generic("Delay ms", default=str(delay)))
        autocal = input_generic("Auto-calibrate filters? (y/n)", default="y" if autocal else "n").lower().startswith('y')

        password = getpass.getpass("Password: ")
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers.append(f"Authorization: Basic {token}")
    elif auth_choice == 'bearer':
        token = getpass.getpass("Bearer token: ")
        headers.append(f"Authorization: Bearer {token}")

    # Target URL
    url = get_target_url(scan_key)
    # Additional options
    threads = int(input_generic("Threads", default="50"))
    status_codes = input_generic("Status codes (comma-separated)", default="200,204,301,403")
    color = input_generic("Color output? (y/n)", default="y").lower().startswith('y')
    autocal = input_generic("Auto-calibrate filters? (y/n)", default="y").lower().startswith('y')
    # Custom Headers
    headers = []
    if input_generic("Add custom HTTP header? (y/n)", default="n").lower().startswith('y'):
        while True:
            h = console.input("Header (Key: Value), blank to stop: ").strip()
            if not h:
                break
            headers.append(h)
    # Proxy
    proxy = ''
    if input_generic("Use proxy? (y/n)", default="n").lower().startswith('y'):
        proxy = console.input("Proxy URL (http://host:port): ").strip()
    # Delay
    delay = 0
    if input_generic("Add delay between requests in ms? (y/n)", default="n").lower().startswith('y'):
        delay = int(input_generic("Delay ms", default="100"))
    # Recursion
    recursion = False
    depth = 1
    if scan_key == '10':
        recursion = True
        depth = int(input_generic("Recursion depth", default="2"))
    # Decoy requests
    decoy = ''
    if input_generic("Use decoy requests? (y/n)", default="n").lower().startswith('y'):
        decoy = console.input("Path to decoy URL list (one per line): ").strip()
    # Output file
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    outfile = f"ffuf_results_{now}.json"
    params = {
        'wordlist': wordlist,
        'url': url,
        'threads': threads,
        'status_codes': status_codes,
        'color': color,
        'autocal': autocal,
        'headers': headers,
        'proxy': proxy,
        'delay': delay,
        'recursion': recursion,
        'depth': depth,
        'decoy': decoy,
        'output': outfile
    }
    cmd = build_command(params)
    res = run_ffuf(cmd)
    summary = None
    if os.path.isfile(outfile):
        summary = parse_results(outfile)
    # History entry
    entry = {
        'timestamp': datetime.now().isoformat(),
        'scan_type': stype,
        'params': params,
        'summary': summary
    }
    update_history(entry)
    console.print(f"Results saved to {outfile}")

if __name__ == '__main__':
    main()
