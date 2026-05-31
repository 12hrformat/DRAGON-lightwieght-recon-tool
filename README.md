# DRAGON Recon CLI 🚀

DRAGON is a lightweight reconnaissance tool built in Python that brings several commonly used recon and enumeration tools together under one interface. Instead of running multiple commands manually, DRAGON helps automate the process and keeps everything organized in one place.

Whether you're doing a quick target overview or gathering information during a security assessment, DRAGON aims to make the workflow faster and more convenient.

## Features

* Automatically checks for required tools on startup.
* Installs or updates missing dependencies when possible.
* Displays a custom `CHECKING` animation and DRAGON banner.
* Run every supported tool at once or choose only the tools you need.
* Save all scan results to a single output file.
* Handles `Ctrl+C` gracefully without leaving a mess behind.

---

## Included Files

| File        | Description                   |
| ----------- | ----------------------------- |
| `dragon.py` | Main application              |
| `dragon`    | Executable launcher           |
| `setup.sh`  | Installation and setup script |

---

## Requirements

* Linux-based operating system
* Python 3
* `apt-get`
* Root privileges

> **Why does DRAGON require root?**
>
> On first launch, DRAGON checks for missing dependencies, updates existing tools when needed, and may install packages automatically. Root privileges are required for these system-level operations. Without elevated permissions, the tool would not be able to manage packages or update its required components.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/12hrformat/DRAGON-lightweight-recon-tool.git
```

Move into the project directory:

```bash
cd DRAGON-lightwieght-recon-tool
```

Run the setup script:

```bash
sudo bash setup.sh
```

After installation, DRAGON will be ready to use.

---

## Usage

### Run a Full Recon Scan

```bash
sudo python3 dragon.py --all -u example.com
```

### Run Specific Tools

```bash
sudo python3 dragon.py -u example.com -t whatweb nslookup dig httpx
```

### Display the DRAGON Banner

```bash
sudo python3 dragon.py --dragon
```

### Save Output to a File

```bash
sudo python3 dragon.py --all -u example.com -o recon_results.txt
```

### Use the Installed Launcher

```bash
sudo dragon --all -u example.com
```

---

## Supported Tools

DRAGON currently supports:

* WhatWeb
* NSLookup
* Dig
* Nuclei
* Amass
* Gobuster
* FFUF
* Nikto
* DirBuster
* HTTPX

More tools may be added in future releases.

---

## Notes

* DRAGON will attempt to install or update supported tools automatically when possible.
* If a package is not available through your system repositories, manual installation may be required.
* Pressing `Ctrl+C` at any time will safely stop execution.
* Results from multiple tools can be combined into a single output file for easier review.

---

## Disclaimer

This project is intended for educational purposes, lab environments, bug bounty programs, and authorized security testing only.

Always ensure you have permission before scanning or testing any system. The user is solely responsible for how this software is used.

---

## Contact

Found a bug? Have an idea for a feature? Feel free to reach out.

Instagram: **@12hrformat**

If you find this project useful, consider giving it a ⭐ on GitHub.
