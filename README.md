
# genfiles

A lightweight command‑line utility for generating test files and directory structures. It supports two modes:

- **Simple Creation Mode**: create *N* fixed‑size binary files in a single root directory.
- **Structured Creation Mode** (default): create *N* subdirectories, each containing 1..*M* files with randomized sizes and (binary/text) types.

The tool is useful for performance testing, storage exercises, demo environments, or teaching materials where synthetic data and predictable structures are required.

---

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Simple Creation Mode](#simple-creation-mode)
  - [Structured Creation Mode](#structured-creation-mode)
  - [Statistics](#statistics)
- [Command‑line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Output Structure](#output-structure)
- [Notes & Behavior](#notes--behavior)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Metadata](#metadata)

---

## Features
- Generate **binary** and **text** files with randomized content.
- Create **fixed‑size** files for deterministic scenarios.
- Build multi‑level **structured directories** for realistic test sets.
- Optional **statistics** summary (counts, totals, averages).
- Clear input validation and helpful console messages.

## Requirements
- Python 3.8+
- Works on Linux, macOS, and Windows (no external dependencies).

## Installation
Clone or download the repository, then run the script directly:

```bash
# Using git
git clone https://github.com/igorbrzezek/genfiles.git
cd genfiles

# Or place genfiles.py somewhere on your PATH
python genfiles.py -h
```

> No third‑party packages are required.

## Usage
Run with Python and provide the **root directory** (`-d/--directory`) plus mode‑specific options.

```text
python genfiles.py -d <ROOT_DIR> [mode options] [--stat]
```

### Simple Creation Mode
Create **N** binary files, each of size **M** kilobytes (KB), in the root directory.

```bash
python genfiles.py -d ./data --file-create N M [--stat]
```

- Files are named `fixed_file_001.bin`, `fixed_file_002.bin`, ...
- Size is deterministic: exactly **M KB** per file.

### Structured Creation Mode
Create **N** subdirectories under the root, and in each subdirectory generate **1..M** files with randomized sizes (min..max) and types.

```bash
python genfiles.py -d ./dataset -n N -m M -k K [--bin | --txt | --mix] [--stat]
```

- `-n` (N): number of subdirectories.
- `-m` (M): maximum number of files per subdirectory (actual count: 1..M).
- `-k` (K): **maximum** file size in KB. Each file size is randomized between **min** and **K** (see *Notes*).
- `--bin` / `--txt` / `--mix`: choose only binary, only text, or a ~50/50 mix (default: `--mix`).

### Statistics
Append `--stat` to print a summary after generation.

- **Simple Mode**: total files, total size (MB), average size (MB).
- **Structured Mode**: counts and total sizes for binary/text, average sizes (KB), overall totals (MB).

## Command‑line Arguments
Below is a concise map of all arguments.

```text
Required for all modes:
  -d, --directory          Name of the root directory to be created

Simple Creation Mode (overrides structured options):
  -fc, --file-create N M   Create N binary files, each of size M KB

Structured Creation Mode (default):
  -n                       Number of subdirectories to create
  -m, --max-files          Maximum number of files (1..M) per subdirectory
  -k, --max-size-kb        Maximum file size in KB
  --bin | --txt | --mix    File type selection (default: --mix)

General:
  --stat                   Print statistics after generation
  -h, --help               Show help and exit
```

## Examples
### 1) Create 10 fixed‑size files (each 256 KB)
```bash
python genfiles.py -d ./lab/data --file-create 10 256 --stat
```
**What you get:**
```
./lab/data/
  fixed_file_001.bin (256 KB)
  ...
  fixed_file_010.bin (256 KB)
```

### 2) Build a mixed dataset: 5 subdirs, up to 8 files each, max size 1024 KB
```bash
python genfiles.py -d ./dataset -n 5 -m 8 -k 1024 --mix --stat
```
**What you get:**
```
./dataset/
  subdir_001/
    file_001.bin (random size)
    file_002.txt (random size)
    ...
  subdir_002/
    ...
  ...
```

### 3) Binary‑only workload with smaller files
```bash
python genfiles.py -d ./workload -n 12 -m 4 -k 128 --bin
```

### 4) Text‑only corpus for parsing tests
```bash
python genfiles.py -d ./corpus -n 3 -m 12 -k 64 --txt --stat
```

## Output Structure
- **Simple Mode**: all files are created directly under `ROOT_DIR` using the pattern `fixed_file_###.bin`.
- **Structured Mode**:
  - Subdirectories: `subdir_001`, `subdir_002`, ... `subdir_N`.
  - Files inside each subdirectory: `file_001.ext`, `file_002.ext`, ... where `ext` is `.bin` (binary) or `.txt` (text).

## Notes & Behavior
- **Random content**
  - Binary data uses `os.urandom()`.
  - Text data uses printable ASCII letters, digits, and whitespace (`\n`, `\t`).
- **Size bounds**
  - In structured mode, sizes are randomized in **bytes** between `min_size_bytes` (default **100 B**) and `K * 1024`.
  - If `min_size_bytes > K*1024`, the code adjusts the minimum to equal the maximum and proceeds.
- **Validation**
  - Simple mode requires **N > 0** and **M > 0**.
  - Structured mode requires `-n`, `-m`, and `-k`, each **> 0**.
- **Console output**
  - Progress logs list created subdirectories and files, including type and size.
  - A final success message confirms completion and (optionally) statistics.

## Troubleshooting
- **Permission errors**: Ensure you have write access to the target `ROOT_DIR` path.
- **Large runs**: For very large `N`, `M`, or `K`, generation may take time and consume disk space—monitor free space.
- **Non‑ASCII text needs**: This tool generates ASCII text only; for UTF‑8 multilingual corpora, extend `generate_random_data()`.

## License
MIT (or project‑specific; update if needed).

## Metadata
- **Author**: Igor Brzezek
- **Version**: 1.0.2
- **Date**: 2025‑12‑09
- **GitHub**: https://github.com/igorbrzezek/genfiles

---

## Developer Notes (for maintainers)
- Entry point: `main()` parses arguments and dispatches to either `create_files_simple()` or `create_structured_files()`.
- Statistics printers: `print_simple_statistics()` and `print_structured_statistics()`.
- Internals use type hints and straightforward `open(..., 'wb')` writes for both binary and text (text is encoded to UTF‑8 bytes).

