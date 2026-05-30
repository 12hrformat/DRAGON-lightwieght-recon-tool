# DRAGON Recon CLI 🚀

A lightweight Python-based reconnaissance automation tool that orchestrates multiple OSINT and enumeration utilities through a single command-line interface.

## Features

* Automatically checks for required reconnaissance tools and installs or updates them using `apt-get` when available.
* Displays a startup `CHECKING` animation and a custom `DRAGON` banner.
* Run all supported tools at once or select specific tools as needed.
* Save combined scan output to a single file for easy review.
* Gracefully handles `Ctrl+C` interruptions with a clean exit message.

---

## Project Structure

* `dragon.py` — Main CLI application
* `dragon` — Executable wrapper for launching the tool
* `setup.sh` — Installation helper script that installs dependencies and creates a system-wide launcher

---

## Requirements

* Linux-based operating system
* Python 3.x
* `apt-get` package manager
* Root privileges (required for automatic tool installation and updates)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/12hrformat/DRAGON-lightweight-recon-tool.git
```

Move into the project directory:

```bash
cd DRAGON-lightweight-recon-tool
```

Run the setup script:

```bash
sudo bash setup.sh
```

The setup script will install available dependencies and create the `dragon` launcher for easier execution.

---

## Usage

### Run All Supported Tools

```bash
sudo python3 dragon.py --all -u example.com
```

### Run Specific Tools

```bash
sudo python3 dragon.py -u example.com -t whatweb nslookup dig httpx
```

### Display Banner and Help Information

```bash
sudo python3 dragon.py --dragon
```

### Save Results to a Custom Output File

```bash
sudo python3 dragon.py --all -u example.com -o recon_results.txt
```

### Use the Installed Wrapper

```bash
sudo dragon --all -u example.com
```

---

## Supported Tools

* whatweb
* nslookup
* dig
* nuclei
* amass
* gobuster
* ffuf
* nikto
* dirbuster
* httpx

---

## Notes

* The application enforces root privileges to allow automatic installation and updating of supported tools.
* Some tools may not be available through the default package repositories. In such cases, manual installation may be required.
* Scan interruptions using `Ctrl+C` are handled gracefully.

---

## Disclaimer

This tool is intended for educational purposes and authorized security testing only. Always obtain proper permission before scanning or testing systems that you do not own or manage.

---

## Contact

If you encounter issues, have suggestions, or would like to contribute:

Instagram: **@12hrformat**
