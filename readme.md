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
mindgrep --intent-list
```

List all supported intents.

```bash
mindgrep "http request" ./src
```

AST‑search for HTTP calls (default tree view).

```bash
mindgrep -V "TODO" . -F txt -N notes
```

Plain‑text search “TODO” in `.txt` files whose name contains “notes”.

```bash
mindgrep "file io" examples -T
```

Styled ASCII table.

```bash
mindgrep shell examples -J
```

JSON output.

```bash
mindgrep regex examples -C 2
```

Show 2 lines of context around each match.

```bash
mindgrep -V "password" . --staged --blame
```

Only staged files, show Git blame.

```bash
mindgrep db examples --stats --report markdown
```

Show summary report in colored Markdown.

```bash
mindgrep json examples --interactive
```

Interactive TUI—select a match to open in your editor.

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
