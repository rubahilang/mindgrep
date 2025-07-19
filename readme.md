<p align="center">
  <img src="https://i.postimg.cc/J7PV5GYn/Chat-GPT-Image-Jul-20-2025-05-47-31-AM.png" alt="MindGrep Banner" />
</p>

---

<p align="center">
  <span style="font-size: 2.5em; font-weight: bold;">MindGrep</span><br/>
  <em>Semantic-aware code search for any codebase</em><br/>
  Quickly find function calls or text patterns with rich output modes, context, Git support, interactive TUI, stats &amp; more.
</p>

---

## 🚀 Installation

**From PyPI**  
```bash
pip install mindgrep
```

**From GitHub (latest)**  
```bash
pip install "git+https://github.com/rubahilang/mindgrep.git"
```

---

## 📦 Usage

```bash
python -m mindgrep --intent-list
```

List all supported intents.

```bash
python -m mindgrep "http request" ./src
```

AST‑search for HTTP calls (default tree view).

```bash
python -m mindgrep -V "TODO" . -F txt -N notes
```

Plain‑text search “TODO” in `.txt` files whose name contains “notes”.

---

## 📖 Example Session

```bash
$> python -m mindgrep --intent-list
Supported intents:
  - async tasks
  - caching
  - cli parsing
  - compression
  - csv
  - database access
  - email sending
  - error handling
  - file encryption
  - file io
  - http request
  - http server
  - image processing
  - json
  - logging
  - regex
  - shell exec
  - socket
  - threading
  - validation
  - xml
  - yaml

$> python -m mindgrep http examples
$>\mindgrep\examples\
└── http_example.py:6,7,8,9

$> python -m mindgrep -V "foxy" examples -F txt -N values
$>\mindgrep\
└── examples\
    └── values.txt:3

$> mindgrep "file io" examples -T
╒════════════════════════════╤════════╤═══════════════════════════════════════════╕
│ Path                       │   Line │ Code                                      │
╞════════════════════════════╪════════╪═══════════════════════════════════════════╡
│ examples\fileio_example.py │      8 │ shutil.copy("temp.txt", "temp_copy.txt")  │
│ examples\fileio_example.py │      9 │ os.rename("temp_copy.txt", "renamed.txt") │
│ examples\fileio_example.py │     10 │ os.remove("temp.txt")                     │
│ examples\fileio_example.py │     11 │ os.remove("renamed.txt")                  │
╘════════════════════════════╧════════╧═══════════════════════════════════════════╛

$> mindgrep shell examples -J
[
  {"path":"examples\\shell_exec_example.py","line":6,"code":"os.system(\"echo 'Hello from os.system'\")"},
  {"path":"examples\\shell_exec_example.py","line":7,"code":"cmd = shlex.split(\"echo Hello from subprocess\")"},
  {"path":"examples\\shell_exec_example.py","line":8,"code":"result = subprocess.run(cmd, capture_output=True, text=True)"}
]

$> python -m mindgrep regex examples -C 1
$>\mindgrep\examples\
└── regex_example.py:3,4,5,6,7

$> python -m mindgrep -V "TODO" examples --staged --blame
⚠️  Not a git repo, ignoring --staged
$>\mindgrep\
└── examples\
    └── values.txt:1

$> python -m mindgrep db examples --stats --report markdown
mindgrep Report
- Time: 2025-07-20 06:00:00.123456
- Files: 1
- Hits:  2

$> mindgrep json examples --interactive

                             mindgrep Interactive                             
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Idx ┃ File                     ┃ Line ┃ Code                               ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   1 │ examples\json_example.py │ 4    │ data = json.loads('{"x":1,"y":2}') │
│   2 │ examples\json_example.py │ 6    │ out = json.dumps(data)             │
└─────┴──────────────────────────┴──────┴────────────────────────────────────┘
Select index to open (ENTER to skip):
```

---

## ⚙️ Features

- **Intent‑based AST search**: `http request`, `file encryption`, `shell exec`, `database access`, and more.  
- **Alias & fuzzy lookup**: query by short names or typos (e.g. `db`, `crypto`).  
- **Plain‑text search** `-V`: any file type, with `-F` (extension) and `-N` (filename) filters.  
- **Output modes**:  
  - Tree view (default),  
  - Table (`-T`),  
  - JSON (`-J`),  
  - Interactive (`--interactive`).  
- **Context lines** `-C`: show lines around each match.  
- **Git integration**: `--staged` safe‑ignore if not a repo; `--blame`.  
- **Stats & Reports**: `--stats` + `--report [markdown|html|json]`, colored output.  
- **Themes**: light/dark (`--theme`).  
- **Standalone**: single script or installable package, no extra config.

---

## 🙌 Contributing

1. Fork & clone  
2. Create a branch  
3. Add features or fix bugs  
4. Submit a Pull Request  

Follow existing style and add tests/examples in `examples/`.
