# DRAGON Recon CLI 🚀

A lightweight Python-based recon automation tool that orchestrates common OSINT and vulnerability enumeration utilities from a single interface.

## What it does

- Checks for required recon tools and installs or updates them via `apt-get` when possible ✅
- Displays a startup `CHECKING` animation and a `DRAGON` banner 🎬
- Supports running all tools or a selected subset ⚡
- Saves combined scan output to a single file 📄
- Handles `Ctrl+C` interrupts gracefully with a friendly exit message ⛔

## Included files 📁

- `dragon.py` — main CLI script
- `dragon` — executable wrapper to launch the CLI from the current folder
- `setup.sh` — helper script to install dependencies and create a symlink for the wrapper

## Requirements ✅

- Linux with `apt-get`
- Python 3
- Root privileges to install or update required tools

## Installation 🛠️

1. Clone or download this repository.

```bash
git clone https://github.com/12hrformat/DRAGON-lightwieght-recon-tool.git
```
2. Open a terminal in the project folder. (The name can be different)

```bash
cd DRAGON-lightwieght-recon-tool.git
```
3. Run the setup script:

```bash
sudo bash setup.sh
```

This should install any missing packages and create a `dragon` wrapper for easier execution.

## Usage

Run the tool with a target URL and selected tools:

```bash
sudo python3 dragon.py --all -u example.com
```

Run only selected tools:

```bash
sudo python3 dragon.py -u example.com -t whatweb nslookup dig httpx
```

Show the banner and help information:

```bash
sudo python3 dragon.py --dragon
```

Save results to a custom file:

```bash
sudo python3 dragon.py --all -u example.com -o recon_results.txt
```

Use the wrapper once installed:

```bash
sudo ./dragon --all -u example.com
```

## Supported tools 🧰

- `whatweb`
- `nslookup`
- `dig`
- `nuclei`
- `amass`
- `gobuster`
- `ffuf`
- `nikto`
- `dirbuster`
- `httpx`

## Notes 💡

- The script enforces running as root so it can install or update tools automatically.
- If a tool is unavailable through `apt`, it will prompt you to install or update it manually.
- `Ctrl+C` is handled with a shutdown message.

## This is an open-source project
## CONTACT ME IF ANY PROBLEM --> INTAGRAM: 12hrformat
