# ai-agent

Simple developer documentation for the current state of the project.

---

## Ownership & project vision

**I own the implementation** of a **custom AI Agent CLI** with the following design:

- **Accepts coding tasks** — You give the agent a task (e.g. “find all Python files in this folder” or “summarize the layout of the project”).
- **Uses predefined functions** — The agent chooses from a fixed set of tools, such as:
  - Scanning/list files in a directory (e.g. `get_files_info`),
  - Reading file content with truncation (e.g. `get_file_content`),
  - and other functions as they are added.
- **Runs until done or stopped** — The agent calls the Gemini API, selects functions, runs them, and repeats until the task is complete or the run is interrupted/fails.
- **Powered by Gemini API** — All reasoning and tool choice go through Google’s Gemini model.

The code in this repository is my implementation of that agent and its tools. The **calculator** directory is an **example code repo** that runs on this CLI (code the agent can work with, run, or reason about). The file-scanning utility and other predefined functions are tools the agent uses; both are documented below.

---

## Overview

This repo currently contains:

- **Agent CLI** (`main.py`) — Entrypoint that talks to the Gemini API. Right now it sends a single user prompt and prints the model response; the full agent loop (task → choose function → execute → repeat) is the intended evolution.
- **Example code repo** — **Calculator** (`calculator/`) — An example codebase that runs on this CLI. The agent can run it, inspect it, or perform coding tasks against it (e.g. run tests, modify code). It provides a small infix calculator CLI and JSON output.
- **Predefined tools** — Implemented for the agent to call:
  - **Directory listing** (`functions/get_files_info.py`) — `get_files_info`: lists directory contents (names, sizes, is_dir) with path-safety so the agent cannot escape the allowed working directory.
  - **File content** (`functions/get_files_content.py`) — `get_file_content`: reads file content up to a character limit (`CHARACTER_LIMIT` in `config.py`), with a truncation message when the file exceeds it.

Python 3.13+, managed with **uv** (see `pyproject.toml` and `uv.lock`).

---

## Project layout

```
ai-agent/
├── main.py                 # AI Agent CLI entrypoint (Gemini API)
├── pyproject.toml          # Project metadata and dependencies
├── pyrightconfig.json      # Type-checker extra paths
├── .env                    # GEMINI_API_KEY (not committed)
├── .gitignore
│
├── calculator/             # Example code repo (runs on this CLI)
│   ├── main.py             # CLI: expression from argv → JSON result
│   ├── tests.py            # unittest for Calculator
│   └── pkg/
│       ├── calculator.py   # Infix expression evaluator (+, -, *, /)
│       └── render.py       # JSON formatting of expression + result
│
└── functions/
    ├── get_files_info.py   # List dir contents; respects working dir boundary
    └── get_files_content.py # Read file content with truncation; path-safe
```

Root-level tests (run from repo root):

- `test_get_files_info.py` — tests for `get_files_info`.
- `test_get_file_content.py` — tests for `get_file_content`.

---

## Setup

1. **Environment**

   - Create a venv (e.g. `uv venv` → `.venv`) and install:  
     `uv sync`
   - Copy or create `.env` with:
     - `GEMINI_API_KEY` — required for `main.py` (Gemini client).

2. **Dependencies** (from `pyproject.toml`)

   - `google-genai` — Gemini API client
   - `python-dotenv` — load `.env` for `main.py`

   Optional: use the project’s `.venv` (ignored by git).

---

## Running

- **Gemini CLI** (from repo root):
  ```bash
  python main.py "Your prompt here"
  python main.py "Your prompt" --verbose   # show token usage
  ```

- **Calculator** — Example code repo that runs on this CLI (from repo root):
  ```bash
  python calculator/main.py "3 + 5"
  python calculator/main.py "2 * 3 - 8 / 2 + 5"
  ```
  Output is JSON: `{"expression": "...", "result": <number>}`. The agent can execute this code or work on it as part of a coding task.

- **Directory listing** (programmatic):
  - `get_files_info(working_directory, directory=".")`  
  - Returns a string of lines: `name : file_size=<bytes>, is_dir=<bool>`.  
  - Restricts listing to paths under `working_directory`; raises if `directory` is outside it or not a directory.

- **File content** (programmatic):
  - `get_file_content(working_directory, file_path)`  
  - Returns file content up to `CHARACTER_LIMIT` characters; appends a truncation message if the file is longer.  
  - Path must be under `working_directory`; raises if outside, not found, or not a regular file.

---

## Testing

- **Calculator** (from repo root):
  ```bash
  python -m pytest calculator/tests.py -v
  # or
  python calculator/tests.py
  ```
  Covers: addition, subtraction, multiplication, division, operator precedence, empty expression, invalid operator, and not enough operands.

- **get_files_info** (from repo root):
  ```bash
  python -m pytest test_get_files_info.py -v
  # or
  python test_get_files_info.py
  ```
  Covers: current dir, subdir (`pkg`), and rejection of `/bin` and `../` (outside permitted working directory); nonexistent path and file-as-path raise.

- **get_file_content** (from repo root):
  ```bash
  python -m pytest test_get_file_content.py -v
  # or
  python test_get_file_content.py
  ```
  Covers: truncation when file exceeds limit, short file and nested path return content below limit, path outside working directory raises, file not found raises.

---

## Implementation notes

- **Calculator** (example code repo)  
  - Tokenizes on spaces; supports `+`, `-`, `*`, `/` with standard precedence (\*, / over +, -).  
  - Uses a stack-based infix evaluator; raises `ValueError` on invalid tokens or malformed expressions.  
  - Lives under `calculator/` as the example codebase that runs on the CLI.

- **get_files_info**  
  - Takes absolute/normalized paths and ensures the target directory is under `working_directory` (no escaping outside the allowed root).  
  - Returns a string of entry lines; errors are raised as exceptions. Skips `.` and `..` in the listing.

- **get_file_content**  
  - Resolves `file_path` under `working_directory`, reads up to `CHARACTER_LIMIT` characters, and appends a truncation message if the file is longer.  
  - Raises if the path is outside the working directory, the file is not found, or it is not a regular file.

- **Type checking**  
  - `pyrightconfig.json` sets `extraPaths: ["."]` so imports like `calculator.pkg`, `functions.get_files_info`, and `functions.get_files_content` resolve from the project root.

---

## Current state summary

| Area            | Status |
|-----------------|--------|
| Agent vision    | Custom AI Agent CLI: accept coding task → choose predefined functions (e.g. scan files) → run until complete or interrupted; Gemini API. |
| Agent entrypoint| `main.py` — Gemini client working; full loop (tool choice + execution + repeat) in progress. |
| Predefined tools | `get_files_info` (directory listing) and `get_file_content` (file reading with truncation) implemented and tested; path safety in place. |
| Example code repo | `calculator/` — Example codebase that runs on the CLI; agent can run/inspect it. |
| Packaging       | `pyproject.toml` + `uv.lock`; no `scripts` entrypoints. |

No web UI or long-running services; everything is CLI or library-style.
