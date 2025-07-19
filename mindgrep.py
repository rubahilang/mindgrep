#!/usr/bin/env python3
import os
import sys
import ast
import json
import argparse
import subprocess
import datetime
from importlib import util as importlib_util

from colorama import init, Fore, Style
from tabulate import tabulate
from rapidfuzz import process
from git import Repo, exc as git_exc
from rich.console import Console
from rich.table import Table

# ──────────────────────────────────────────────────
init(autoreset=True)
RESET = Style.RESET_ALL

# Default intents & AST patterns
INTENT_PATTERNS = {
    # HTTP clients & requests
    "http request": [
        "requests.get", "requests.post", "requests.put", "requests.delete",
        "requests.head", "requests.options", "requests.patch",
        "requests.Session", "requests.request",
        "urllib.request.urlopen", "urllib3.PoolManager.request",
        "http.client.HTTPConnection", "http.client.HTTPSConnection",
        "httpx.get", "httpx.post", "httpx.put", "httpx.delete", "httpx.request",
        "aiohttp.ClientSession.get", "aiohttp.ClientSession.post", "aiohttp.request",
        "tornado.httpclient.AsyncHTTPClient.fetch",
        "tornado.httpclient.HTTPClient.fetch",
    ],

    # File/data encryption & hashes
    "file encryption": [
        "cryptography.fernet.Fernet", "Fernet(",
        "AES.new", "Crypto.Cipher.AES.new",
        "Crypto.Cipher.ChaCha20.new", "ChaCha20Poly1305.new",
        "hashlib.md5", "hashlib.sha256", "hashlib.sha512", "hashlib.blake2b",
        "hmac.new", "hashlib.pbkdf2_hmac", "scrypt",
        "rsa.encrypt", "RSA.import_key", "Crypto.PublicKey.RSA.generate",
    ],

    # Shell / OS command execution
    "shell exec": [
        "os.system", "os.popen", "subprocess.run", "subprocess.Popen",
        "subprocess.call", "subprocess.check_output", "subprocess.check_call",
        "subprocess.Popen(shell=True", "commands.getoutput",
        "pexpect.spawn", "shlex.split", "fabric.Connection", "paramiko.SSHClient",
    ],

    # Databases & key‐value stores
    "database access": [
        "sqlite3.connect", "psycopg2.connect", "pymysql.connect",
        "mysql.connector.connect", "sqlalchemy.create_engine",
        "cursor.execute", "engine.execute",
        "pymongo.MongoClient", "redis.Redis",
        "motor.motor_asyncio.AsyncIOMotorClient",
        "boto3.resource('dynamodb')", "boto3.client('dynamodb')",
        "neo4j.GraphDatabase.driver", "elasticsearch.Elasticsearch",
    ],

    # File system & I/O
    "file io": [
        "open(", "Path.open(", "Path.write_text", "Path.read_text",
        "os.remove", "os.unlink", "os.rename",
        "os.mkdir", "os.makedirs", "shutil.copy", "shutil.move",
        "shutil.rmtree", "tempfile.NamedTemporaryFile",
        "tempfile.TemporaryDirectory", "glob.glob", "os.walk",
    ],

    # JSON serialization
    "json": [
        "json.load", "json.loads", "json.dump", "json.dumps",
        "simplejson.loads", "simplejson.dumps",
        "ujson.loads", "ujson.dumps",
    ],

    # XML parsing
    "xml": [
        "xml.etree.ElementTree.parse", "xml.etree.ElementTree.fromstring",
        "lxml.etree.parse", "lxml.objectify.fromstring",
        "xml.dom.minidom.parseString", "xml.sax.make_parser",
        "bs4.BeautifulSoup", "BeautifulSoup(",
    ],

    # YAML parsing
    "yaml": [
        "yaml.safe_load", "yaml.load", "yaml.FullLoader", "yaml.RoundTripLoader",
        "ruamel.yaml.YAML().load", "ruamel.yaml.round_trip_load",
    ],

    # CSV & tabular
    "csv": [
        "csv.reader", "csv.writer", "csv.DictReader", "csv.DictWriter",
        "pandas.read_csv", "pandas.DataFrame.to_csv",
        "numpy.loadtxt", "numpy.savetxt",
    ],

    # Regular expressions
    "regex": [
        "re.search", "re.match", "re.findall", "re.sub", "re.compile",
        "regex.search", "regex.match",
    ],

    # Logging & print
    "logging": [
        "logging.debug", "logging.info", "logging.warning",
        "logging.error", "logging.critical", "logger.log",
        "print(", "warnings.warn", "sys.stderr.write",
    ],

    # Concurrency: threads & processes
    "threading": [
        "threading.Thread", "concurrent.futures.ThreadPoolExecutor",
        "concurrent.futures.ProcessPoolExecutor",
        "multiprocessing.Process", "multiprocessing.Pool",
        "multiprocessing.dummy.Pool",
    ],

    # Async libraries
    "async tasks": [
        "asyncio.create_task", "asyncio.run", "asyncio.gather",
        "asyncio.ensure_future", "trio.run", "curio.run", "anyio.run",
    ],

    # Sockets & websockets
    "socket": [
        "socket.socket", "socket.bind", "socket.listen", "socket.connect",
        "ssl.wrap_socket", "ssl.SSLContext", "asyncio.open_connection",
        "asyncio.start_server", "websockets.connect", "websockets.serve",
    ],

    # HTTP/server frameworks
    "http server": [
        "http.server.HTTPServer", "http.server.SimpleHTTPRequestHandler",
        "flask.Flask", "FastAPI(", "django.urls", "Sanic(",
        "bottle.Bottle", "tornado.web.Application", "aiohttp.web.Application",
    ],

    # Compression & archives
    "compression": [
        "zipfile.ZipFile", "tarfile.open", "gzip.open",
        "bz2.BZ2File", "lzma.open", "shutil.make_archive",
        "patoolib.extract_archive",
    ],

    # Image processing
    "image processing": [
        "PIL.Image.open", "PIL.Image.save", "cv2.imread", "cv2.imwrite",
        "cv2.VideoCapture", "skimage.io.imread", "skimage.io.imsave",
        "Image.fromarray", "matplotlib.pyplot.imshow",
    ],

    # CLI parsing
    "cli parsing": [
        "argparse.ArgumentParser", "click.command", "typer.Typer",
        "optparse.OptionParser", "docopt.docopt", "sys.argv",
    ],

    # Caching layers
    "caching": [
        "functools.lru_cache", "cachetools.Cache", "django.core.cache",
        "redis_cache.Cache", "dogpile.cache", "memcache.Client",
    ],

    # Tambahan umum:
    "email sending": [
        "smtplib.SMTP", "smtplib.SMTP_SSL",
        "email.mime.text.MIMEText", "EmailMessage",
        "yagmail.SMTP", "send_email",
    ],
    "validation": [
        "pydantic.BaseModel", "validate_email", "cerberus.Validator",
        "marshmallow.Schema", "jsonschema.validate",
    ],
    "authentication": [
        "jwt.encode", "jwt.decode", "pyjwt.decode",
        "werkzeug.security", "bcrypt.hashpw", "bcrypt.checkpw",
    ],
    "error handling": [
        "try:", "except", "finally:", "raise", "assert", "logging.exception",
    ],
}


INTENT_ALIASES = {
    "http request":       ["http", "url", "req", "request", "httpx", "urllib"],
    "file encryption":    ["encrypt", "crypto", "AES", "Fernet", "KDF", "hash"],
    "shell exec":         ["shell", "exec", "bash", "sh", "system", "cmd", "subprocess"],
    "database access":    ["database", "db", "sql", "nosql", "mongo", "redis"],
    "file io":            ["file", "io", "fs", "filesystem", "path", "read", "write"],
    "json":               ["json", "serialize", "deserialize", "simplejson", "ujson"],
    "xml":                ["xml", "xslt", "dom", "sax", "beautifulsoup", "bs4", "lxml"],
    "yaml":               ["yaml", "yml", "config", "settings", "ruamel"],
    "csv":                ["csv", "table", "spreadsheet", "tsv", "pandas", "numpy"],
    "regex":              ["regex", "re", "pattern", "regexp"],
    "logging":            ["log", "logger", "warning", "error", "print"],
    "threading":          ["thread", "threads", "parallel", "multiprocessing"],
    "async tasks":        ["async", "asyncio", "trio", "curio", "anyio"],
    "socket":             ["socket", "ssl", "websocket", "tcp", "udp"],
    "http server":        ["server", "flask", "fastapi", "django", "sanic", "bottle"],
    "compression":        ["zip", "tar", "gzip", "bz2", "lzma", "archive", "compress"],
    "image processing":   ["image", "pil", "opencv", "cv2", "skimage", "matplotlib"],
    "cli parsing":        ["cli", "argparse", "click", "typer", "optparse", "docopt"],
    "caching":            ["cache", "caching", "lru", "redis", "memcache", "dogpile"],
    "email sending":      ["email", "smtp", "mail", "yagmail", "messaging"],
    "validation":         ["validate", "schema", "pydantic", "cerberus", "marshmallow", "jsonschema"],
    "authentication":     ["auth", "jwt", "oauth", "token", "login", "bcrypt"],
    "error handling":     ["error", "exception", "assert", "raise", "try", "catch"],
}

ALIAS_MAP = {
    alias.lower(): intent
    for intent, aliases in INTENT_ALIASES.items()
    for alias in aliases
}

# Theme definitions
THEMES = {
    "light": {
        "dir":        Fore.CYAN + Style.BRIGHT,
        "file":       Fore.GREEN + Style.BRIGHT,
        "line":       Fore.YELLOW,
        "code":       Fore.WHITE,
        "conn":       Fore.MAGENTA,
        "stat_hdr":   Fore.CYAN + Style.BRIGHT,
        "stat_val":   Fore.YELLOW,
    },
    "dark": {
        "dir":        Fore.BLUE + Style.BRIGHT,
        "file":       Fore.WHITE + Style.BRIGHT,
        "line":       Fore.MAGENTA,
        "code":       Fore.WHITE,
        "conn":       Fore.YELLOW,
        "stat_hdr":   Fore.CYAN + Style.BRIGHT,
        "stat_val":   Fore.YELLOW,
    },
}
DIR_COLOR = FILE_COLOR = LINE_COLOR = CODE_COLOR = CONN_COLOR = ""
STAT_HDR = STAT_VAL = ""

def apply_theme(name):
    global DIR_COLOR, FILE_COLOR, LINE_COLOR, CODE_COLOR, CONN_COLOR, STAT_HDR, STAT_VAL
    th = THEMES.get(name, THEMES["light"])
    DIR_COLOR  = th["dir"]
    FILE_COLOR = th["file"]
    LINE_COLOR = th["line"]
    CODE_COLOR = th["code"]
    CONN_COLOR = th["conn"]
    STAT_HDR   = th["stat_hdr"]
    STAT_VAL   = th["stat_val"]

# ──────────────────────────────────────────────────
def load_plugins():
    plugins = {}
    pd = os.path.join(os.path.dirname(__file__), "plugins")
    if os.path.isdir(pd):
        for fn in sorted(os.listdir(pd)):
            if fn.endswith(".py"):
                path = os.path.join(pd, fn)
                spec = importlib_util.spec_from_file_location(fn, path)
                mod  = importlib_util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                plugins[fn[:-3]] = mod
    return plugins

# AST helpers
def get_full_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = get_full_name(node.value)
        return f"{parent}.{node.attr}"
    return None

def scan_file_ast(fp, patterns):
    try:
        src  = open(fp, encoding="utf-8", errors="ignore").read()
        tree = ast.parse(src, filename=fp)
    except Exception:
        return []
    hits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            nm = get_full_name(n.func)
            if nm in patterns:
                ln   = n.lineno
                code = src.splitlines()[ln-1].strip()
                hits.append((ln, code))
    return hits

def find_intent_matches(intent, root, file_ext=None, name_filter=None):
    patterns = INTENT_PATTERNS[intent]
    matches, results = {}, []
    ext = file_ext.lstrip(".").lower() if file_ext else None

    for dp, _, files in os.walk(root):
        for fn in sorted(files):
            low = fn.lower()
            if ext:
                if not low.endswith(f".{ext}"):
                    continue
            else:
                if not low.endswith(".py"):
                    continue
            if name_filter and name_filter.lower() not in low:
                continue
            full = os.path.join(dp, fn)
            hits = scan_file_ast(full, patterns)
            if hits:
                matches[full] = hits
                for ln, code in hits:
                    results.append({"path": full, "line": ln, "code": code})
    return matches, results

# Plain‑text search
def search_value(val, root, file_ext=None, name_filter=None):
    ext = file_ext.lstrip(".").lower() if file_ext else None
    lowval = val.lower()
    matches, results = {}, []

    for dp, _, files in os.walk(root):
        for fn in sorted(files):
            low = fn.lower()
            if ext:
                if not low.endswith(f".{ext}"):
                    continue
            if name_filter and name_filter.lower() not in low:
                continue
            full = os.path.join(dp, fn)
            try:
                for i, line in enumerate(open(full, encoding="utf-8", errors="ignore"), 1):
                    if lowval in line.lower():
                        c = line.strip()
                        matches.setdefault(full, []).append((i, c))
                        results.append({"path": full, "line": i, "code": c})
            except Exception:
                continue
    return matches, results

# Context lines
def with_context(path, lineno, ctx=3):
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    start, end = max(1, lineno-ctx), min(len(lines), lineno+ctx)
    return [(i, lines[i-1].rstrip()) for i in range(start, end+1)]

# Fuzzy intent resolution
def resolve_intent(q, intents):
    match, score, _ = process.extractOne(q, intents)
    return match if score >= 60 else None

# Git integration
def get_staged_files(rp):
    try:
        repo = Repo(rp, search_parent_directories=True)
        return [i.a_path for i in repo.index.diff("HEAD")]
    except git_exc.InvalidGitRepositoryError:
        print(f"{Fore.YELLOW}⚠️  Not a git repo, ignoring --staged{RESET}")
        return None

def get_blame(path, lineno):
    try:
        repo = Repo(path, search_parent_directories=True)
        rel  = os.path.relpath(path, repo.working_tree_dir)
        commit, _ = repo.blame("HEAD", rel)[lineno-1]
        return commit, _
    except Exception:
        return None, None

# Metrics & reporting
def stats(matches):
    return {
        "timestamp": str(datetime.datetime.now()),
        "files":     len(matches),
        "hits":      sum(len(v) for v in matches.values()),
    }

def export_report(data, fmt="markdown"):
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt == "html":
        return (
            "<html><body>"
            f"<h1>mindgrep Report</h1>"
            f"<ul><li>Time: {data['timestamp']}</li>"
            f"<li>Files: {data['files']}</li>"
            f"<li>Hits: {data['hits']}</li></ul>"
            "</body></html>"
        )
    # markdown default
    return (
        f"**mindgrep Report**\n"
        f"- Time: {data['timestamp']}\n"
        f"- Files: {data['files']}\n"
        f"- Hits:  {data['hits']}\n"
    )

def print_report(data, fmt="markdown"):
    if fmt == "json":
        print(export_report(data, "json"))
    elif fmt == "html":
        print(export_report(data, "html"))
    else:
        print(f"{STAT_HDR}mindgrep Report{RESET}")
        print(f"{STAT_HDR}- Time:{RESET} {STAT_VAL}{data['timestamp']}{RESET}")
        print(f"{STAT_HDR}- Files:{RESET} {STAT_VAL}{data['files']}{RESET}")
        print(f"{STAT_HDR}- Hits:{RESET}  {STAT_VAL}{data['hits']}{RESET}")

# Interactive TUI
def interactive_view(matches):
    console = Console()
    table   = Table(title="mindgrep Interactive")
    table.add_column("Idx", justify="right")
    table.add_column("File")
    table.add_column("Line")
    table.add_column("Code")

    rows = []
    idx = 1
    for path, hits in matches.items():
        for ln, code in hits:
            table.add_row(str(idx), path, str(ln), code)
            rows.append((path, ln))
            idx += 1

    console.print(table)
    choice = console.input("Select index to open (ENTER to skip): ")

    if not choice.isdigit():
        return

    sel = int(choice) - 1
    if not (0 <= sel < len(rows)):
        color_error("⚠️  Invalid selection")
        return

    file_path, line_no = rows[sel]

    # Tentukan editor
    if os.name == "nt":
        editor = os.environ.get("EDITOR", "notepad")
        args = [editor, file_path]               # Notepad buka tanpa +line
    else:
        editor = os.environ.get("EDITOR", "vim")
        args = [editor, f"+{line_no}", file_path]

    console.print(f"Opening {file_path}:{line_no} in {editor}")

    try:
        subprocess.run(args)
    except FileNotFoundError:
        color_error(f"⚠️  Editor '{editor}' not found. Please set the EDITOR env var.")


# Utilities
def color_error(msg):
    print(f"{Fore.RED}{Style.BRIGHT}{msg}{RESET}")

def build_tree(matches, root):
    tree = {}
    for full, hits in matches.items():
        rel = os.path.relpath(full, root)
        parts = rel.split(os.sep)
        node = tree
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        nums = [ln for ln, _ in hits]
        node.setdefault(parts[-1], []).extend(nums)
    return tree

def print_tree(tree, prefix=""):
    items = list(tree.items())
    for i, (name, val) in enumerate(items):
        last = (i == len(items)-1)
        conn = f"{CONN_COLOR}{'└──' if last else '├──'}{RESET}"
        if isinstance(val, dict):
            print(f"{prefix}{conn} {DIR_COLOR}{name}{os.sep}{RESET}")
            ext = "    " if last else "│   "
            print_tree(val, prefix + ext)
        else:
            nums = ",".join(str(n) for n in sorted(set(val)))
            print(f"{prefix}{conn} {FILE_COLOR}{name}{RESET}:{LINE_COLOR}{nums}{RESET}")

def output_table(matches):
    rows = []
    for p, hits in matches.items():
        for ln, c in hits:
            rows.append([p, ln, c])
    if not rows:
        print("(no matches)")
        return
    hdr = [STAT_HDR + h + RESET for h in ["Path", "Line", "Code"]]
    clr = [[r[0], f"{STAT_VAL}{r[1]}{RESET}", f"{CODE_COLOR}{r[2]}{RESET}"] for r in rows]
    print(tabulate(clr, headers=hdr, tablefmt="fancy_grid"))

# ──────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(prog="mindgrep", description="semantic grep for Python (fixed)")
    p.add_argument("intent", nargs="?", help="intent name (ignored if -V)")
    p.add_argument("path",   nargs="?", default=".", help="root folder to scan")
    p.add_argument("-V","--value",    metavar="VAL", help="plain-text search")
    p.add_argument("-T","--table",    action="store_true", help="styled table")
    p.add_argument("-J","--json",     action="store_true", help="JSON output")
    p.add_argument("-F","--file",     dest="file_ext",    help="filter by extension")
    p.add_argument("-N","--name",     dest="name_filter", help="filter by filename")
    p.add_argument("-C","--context",  type=int, default=0,   help="context lines")
    p.add_argument("--staged",        action="store_true",  help="scan staged only")
    p.add_argument("--blame",         action="store_true",  help="show git blame")
    p.add_argument("--stats",         action="store_true",  help="show stats")
    p.add_argument("--report",        choices=["markdown","html","json"], help="export report")
    p.add_argument("--interactive",   action="store_true",  help="interactive mode")
    p.add_argument("--intent-list",   action="store_true",  help="list intents")
    p.add_argument("--theme",         choices=["light","dark"], default="light", help="color theme")
    args = p.parse_args()

    apply_theme(args.theme)
    plugins = load_plugins()

    if args.intent_list:
        print("Supported intents:")
        for i in sorted(INTENT_PATTERNS):
            print("  -", i)
        sys.exit(0)

    root = args.path
    staged = get_staged_files(os.getcwd()) if args.staged else None

    if args.value:
        matches, results = search_value(args.value, root, args.file_ext, args.name_filter)
    else:
        if not args.intent:
            p.print_help()
            sys.exit(1)
        q = args.intent.lower()
        intent = ALIAS_MAP.get(q) or resolve_intent(q, list(INTENT_PATTERNS))
        if not intent:
            color_error(f"⚠️  Intent `{args.intent}` not found")
            sys.exit(1)
        matches, results = find_intent_matches(intent, root, args.file_ext, args.name_filter)

    if staged is not None:
        matches = {p:h for p,h in matches.items() if os.path.relpath(p, root) in staged}
        results = [r for r in results if r["path"] in matches]

    if not matches:
        if args.json:
            print("[]")
        else:
            color_error("⚠️  No files matched your criteria!")
        sys.exit(0)

    if args.context:
        ctx = {}
        for p, hits in matches.items():
            ctx[p] = []
            for ln, _ in hits:
                ctx[p].extend(with_context(p, ln, args.context))
        matches = ctx
        results = [{"path":p, "line":ln, "code":c} for p,h in ctx.items() for ln,c in h]

    if args.blame:
        for r in results:
            commit, _ = get_blame(r["path"], r["line"])
            if commit:
                r["blame"] = {"commit": commit.hexsha, "author": commit.author.name}

    if args.stats:
        s = stats(matches)
        if args.json:
            print(json.dumps(s, indent=2))
        else:
            fmt = args.report or "markdown"
            print_report(s, fmt)
        sys.exit(0)

    if args.interactive:
        interactive_view(matches)
        sys.exit(0)

    if args.json:
        print(json.dumps(results, indent=2))
    elif args.table:
        output_table(matches)
    else:
        print(f"{DIR_COLOR}{os.path.abspath(root)}{os.sep}{RESET}")
        tree = build_tree(matches, root)
        print_tree(tree)

if __name__ == "__main__":
    main()
