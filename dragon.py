#!/usr/bin/env python3
#IMPORTING TIMEE
#MADE BY DRAGON
#PLEASE DONT STELA I SPENT TIME ON THIS
#if you wanna however support me or make some changes you can contact me on discord (atmoic._dragon)
#HOURS WASTED ON THIS------> 2

import time
import argparse
import os
import subprocess
import threading
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_OUTPUT = "recon_output.txt"
DEFAULT_WORDLIST = "/usr/share/wordlists/dirb/common.txt"
DEFAULT_SUBDOMAIN_WORDLIST = "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
FIRST_RUN_MARKER = Path(__file__).resolve().parent / ".dragon_initialized"

ANSI_RED = "\033[1;31m"
ANSI_GREEN = "\033[1;32m"
ANSI_YELLOW = "\033[1;33m"
ANSI_CYAN = "\033[1;36m"
ANSI_MAGENTA = "\033[1;35m"
ANSI_RESET = "\033[0m"
#TOOLS
TOOL_ALIASES = {
    "amaas": "amass",
    "fuff": "ffuf",
    "ffuf": "ffuf",
    "gobuster": "gobuster",
    "whatweb": "whatweb",
    "nslookup": "nslookup",
    "dig": "dig",
    "nuclei": "nuclei",
    "nikto": "nikto",
    "dirbuster": "dirbuster",
    "id": "httpx",
}

TOOL_COMMANDS = {
    "nikto": ["nikto", "-host"],
    "gobuster": ["gobuster", "dns", "-d"],
    "ffuf": ["ffuf", "-u"],
    "whatweb": ["whatweb"],
    "nslookup": ["nslookup"],
    "dig": ["dig"],
    "nuclei": ["nuclei", "-u"],
    "amass": ["amass", "enum", "-d"],
    "dirbuster": ["dirbuster", "-u"],
    "httpx": ["httpx", "-silent", "-title", "-u"],
}

TOOL_PRIORITY = {
    "dig": 0,
    "nslookup": 1,
    "whatweb": 2,
    "httpx": 3,
    "nuclei": 4,
    "amass": 5,
    "gobuster": 6,
    "ffuf": 7,
    "nikto": 8,
    "dirbuster": 9,
}


def is_first_run() -> bool:
    return not FIRST_RUN_MARKER.exists()


def mark_first_run_complete() -> None:
    try:
        FIRST_RUN_MARKER.write_text("initialized\n", encoding="utf-8")
    except OSError:
        pass

#Bruh ts is the anner what do ya expact
ASCII_BANNER = r"""
╔═══════════════════════════════════════════════════════════════╗
║     ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗      ║
║     ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║      ║
║     ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║      ║
║     ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║      ║
║     ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║      ║
║      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝     ║
║                                                               ║
║                                                               ║
║    A script that links tools together with style and speed.   ║
║   made by a 14 yo, consider supporting instagram: 12hrformat  ║
╚═══════════════════════════════════════════════════════════════╝
"""


def color_text(text: str, color: str) -> str:
    return f"{color}{text}{ANSI_RESET}"


def display_banner() -> None:
    for line in ASCII_BANNER.strip().splitlines():
        print(color_text(line, ANSI_CYAN), flush=True)
        time.sleep(0.03)
    print(color_text("★ Recon CLI for DRAGON: save all tool output to a single file. ★", ANSI_GREEN), flush=True)
    print()


def display_checking() -> None:
    checking_art = [
        r" ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗",
        r"██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝",
        r"██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗",
        r"██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║",
        r"╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝",
        r" ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝",
    ]
    for line in checking_art:
        print(color_text(line, ANSI_YELLOW), flush=True)
        time.sleep(0.04)

    # Use Spinner to animate during the verification dots
    try:
        spinner = Spinner("Verifying tools")
        spinner.start()
        dots = 0
        for _ in range(8):
            spinner.message = f"Verifying tools{'.' * dots}"
            dots = (dots + 1) % 4
            time.sleep(0.4)
    finally:
        try:
            spinner.stop()
        except Exception:
            pass
    print()


def display_check_results(results: dict[str, str]) -> None:
    """Print per-tool check results after installation attempts."""
    if not results:
        return
    print()
    print(color_text("Dependency check results:", ANSI_CYAN))
    for tool in sorted(results.keys(), key=lambda t: TOOL_PRIORITY.get(t, 999)):
        status = results[tool]
        if status == "present":
            print(color_text(f"[OK]     {tool}", ANSI_GREEN))
        elif status == "installed":
            print(color_text(f"[INST]   {tool} (installed)", ANSI_GREEN))
        elif status == "installed_but_not_found":
            print(color_text(f"[WARN]   {tool} installed but executable not found", ANSI_YELLOW))
        elif status == "no_package_map":
            print(color_text(f"[MANUAL] {tool} has no apt package; install/update manually.", ANSI_YELLOW))
        elif status == "apt_failed":
            print(color_text(f"[FAILED] {tool} apt install failed or package unavailable; install/update manually.", ANSI_RED))
        else:
            print(color_text(f"[MISSING] {tool}", ANSI_RED))
    print()

#Thigs to print when the script first loads
def show_dragon_info() -> None:
    display_banner()
    print(color_text("Usage:", ANSI_YELLOW))
    print("  python3 dragon.py --all -u example.com #<-------uses all tools (recommended)")
    print("  python3 dragon.py -u example.com -t whatweb nslookup dig httpx #<------tool selection custom")
    print("  python3 dragon.py -t id")
    print("  python3 dragon.py --dragon")
    print("  python3 dragon.py --all -u example.com -o recon_results.txt #<--------saves results to a file (you can change the name)")
    print()
    print(color_text("Supported tools:", ANSI_GREEN))
    print("  " + ", ".join(sorted(TOOL_COMMANDS.keys())))
    print()
    print(color_text("Aliases:", ANSI_GREEN))
    print("  amaas -> amass, fuff -> ffuf, id -> httpx")
    print()
    print(color_text("Notes:", ANSI_MAGENTA))
    print("  Type dragon anywhere in the command line to use this tool")
    print("  If you want a direct command name, install a symlink or alias named dragon.")
    print("  Use --all to run every tool automatically.")
    print("  Use --quiet to keep terminal output minimal and still save results to file.")
    print()


def should_show_dragon_info() -> bool:
    args = [arg.lower() for arg in sys.argv[1:]]
    return "--dragon" in args


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
        parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    return url.rstrip("/")


def normalize_domain(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc:
        return parsed.netloc
    raise ValueError(f"Unable to extract domain from URL: {url}")


PACKAGE_MAP = {
    "nikto": "nikto",
    "gobuster": "gobuster",
    "ffuf": "ffuf",
    "whatweb": "whatweb",
    "nslookup": "dnsutils",
    "dig": "dnsutils",
    "nuclei": "nuclei",
    "amass": "amass",
    "dirbuster": "dirbuster",
    "httpx": "httpx",
}


def check_tool_installed(command: str) -> bool:
    return shutil.which(command) is not None


def ensure_root() -> None:
    if os.geteuid() != 0:
        print(color_text("ERROR\nPlease note this script must be run as root, otherwise it wont be able to install and update tools ", ANSI_RED), file=sys.stderr)
        sys.exit(1)


def install_packages(packages: list[str], upgrade_only: bool = False) -> None:
    if not packages:
        return
    packages = sorted(set(packages))
    action = "updating" if upgrade_only else "installing"
    print(color_text(f"{action.capitalize()}: {', '.join(packages)}", ANSI_YELLOW), flush=True)
    subprocess.run(["apt-get", "update"], check=False)
    cmd = ["apt-get", "install", "-y"]
    if upgrade_only:
        cmd.append("--only-upgrade")
    cmd.extend(packages)
    subprocess.run(cmd, check=False)


def install_package(package: str, upgrade_only: bool = False) -> bool:
    """Install a single package via apt-get. Returns True on success."""
    if shutil.which("apt-get") is None:
        return False
    cmd = ["apt-get", "install", "-y"]
    if upgrade_only:
        cmd.append("--only-upgrade")
    cmd.append(package)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode == 0


def ensure_tools_installed(first_run: bool = False) -> dict[str, str]:
    if shutil.which("apt-get") is None:
        print(color_text("apt-get not found; cannot install missing tools automatically.", ANSI_RED), file=sys.stderr)
        return {}

    if first_run:
        print(color_text("First boot detected. Running apt update + upgrade...", ANSI_YELLOW), flush=True)
        subprocess.run(["apt-get", "update"], check=False)
        subprocess.run(["apt-get", "upgrade", "-y"], check=False)
    else:
        print(color_text("Skipping full apt update/upgrade on subsequent runs.", ANSI_YELLOW), flush=True)

    # results: tool -> status
    results: dict[str, str] = {}
    missing_tools: list[str] = []
    for tool in TOOL_COMMANDS:
        check_name = TOOL_COMMANDS[tool][0] if tool != "httpx" else "httpx"
        if check_tool_installed(check_name):
            results[tool] = "present"
        else:
            results[tool] = "missing"
            missing_tools.append(tool)

    # Try installing missing tools one-by-one and record outcome
    if missing_tools:
        print()
        for tool in missing_tools:
            pkg = PACKAGE_MAP.get(tool)
            if not pkg:
                results[tool] = "no_package_map"
                print(color_text(f"{tool}: no apt package mapping; install/update manually.", ANSI_YELLOW))
                continue
            print(color_text(f"Attempting to install {pkg} for {tool}...", ANSI_YELLOW), flush=True)
            ok = install_package(pkg, upgrade_only=False)
            if ok:
                # re-check executable
                check_name = TOOL_COMMANDS[tool][0] if tool != "httpx" else "httpx"
                if check_tool_installed(check_name):
                    results[tool] = "installed"
                    print(color_text(f"{tool}: installed successfully.", ANSI_GREEN))
                else:
                    results[tool] = "installed_but_not_found"
                    print(color_text(f"{tool}: installed but executable not found in PATH.", ANSI_RED))
            else:
                results[tool] = "apt_failed"
                print(color_text(f"{tool}: apt failed to install {pkg}; it is unavailable via apt; install/update manually.", ANSI_RED))

    # Attempt to upgrade known packages, but tolerate failures
    for tool, pkg in PACKAGE_MAP.items():
        print(color_text(f"Updating {pkg}...", ANSI_YELLOW), end="\r", flush=True)
        _ = install_package(pkg, upgrade_only=True)

    return results


def resolve_tool(tool_name: str) -> str:
    return TOOL_ALIASES.get(tool_name.lower(), tool_name.lower())


def order_tools(tools: list[str]) -> list[str]:
    seen = []
    for tool in tools:
        if tool not in seen:
            seen.append(tool)
    return sorted(seen, key=lambda tool: TOOL_PRIORITY.get(tool, 999))


def build_command(tool: str, target_url: str, domain: str, args: argparse.Namespace) -> list[str]:
    command = TOOL_COMMANDS[tool].copy()

    if tool == "nikto":
        command.append(target_url)
    elif tool == "gobuster":
        command.extend([domain, "-w", args.gobuster_wordlist or DEFAULT_SUBDOMAIN_WORDLIST])
    elif tool == "ffuf":
        fuzz_target = f"{target_url}/FUZZ"
        command.extend([fuzz_target, "-w", args.ffuf_wordlist or DEFAULT_WORDLIST, "-mc", "all"])
    elif tool == "whatweb":
        command.append(target_url)
    elif tool == "nslookup":
        command.append(domain)
    elif tool == "dig":
        command.extend([domain, "+short"])
    elif tool == "nuclei":
        command.append(target_url)
    elif tool == "amass":
        command.extend([domain, "-o", "-" ] if "-o" not in command else [domain])
    elif tool == "httpx":
        command.append(target_url)
    elif tool == "dirbuster":
        command.extend([target_url, "-l", args.dirbuster_wordlist or DEFAULT_WORDLIST])
    return command


class Spinner:
    def __init__(self, message: str = "working") -> None:
        self.message = message
        self.chars = ["|", "/", "-", "\\"]
        self.index = 0
        self.running = False
        self.thread = None

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.spin, daemon=True)
        self.thread.start()

    def spin(self) -> None:
        while self.running:
            sys.stdout.write(f"\r{self.message} {self.chars[self.index]} ")
            sys.stdout.flush()
            self.index = (self.index + 1) % len(self.chars)
            time.sleep(0.12)
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()

    def stop(self) -> None:
        self.running = False
        if self.thread:
            self.thread.join()


def run_tool(tool: str, target_url: str, domain: str, args: argparse.Namespace) -> tuple[str, str]:
    if tool not in TOOL_COMMANDS:
        return "", f"[WARNING] Unsupported tool: {tool}"

    executable = TOOL_COMMANDS[tool][0]
    if not check_tool_installed(executable):
        return "", f"[WARNING] {executable} is not installed or not found in PATH."

    command = build_command(tool, target_url, domain, args)
    header = f"=== {tool.upper()} COMMAND: {' '.join(command)} ==="

    output_lines = []
    spinner = Spinner(f"[{tool.upper()}] working") if not args.quiet else None
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except OSError as exc:
        return header, f"[ERROR] failed to start {tool}: {exc}"

    try:
        if spinner:
            spinner.start()
        assert process.stdout is not None
        for line in process.stdout:
            clean = line.rstrip("\n")
            output_lines.append(clean)
            if spinner:
                spinner.stop()
            if not args.quiet:
                print(color_text(f"[{tool.upper()}] {clean}", ANSI_YELLOW), flush=True)
            if spinner:
                spinner = Spinner(f"[{tool.upper()}] working")
                spinner.start()
        exit_code = process.wait(timeout=1800)
    except subprocess.TimeoutExpired as exc:
        if spinner:
            spinner.stop()
        process.kill()
        return header, f"[ERROR] {tool} timed out: {exc}"
    finally:
        if spinner:
            spinner.stop()

    body = "\n".join(output_lines).strip()
    if not body:
        body = "(no stdout output)"
    if exit_code != 0 and body:
        body += f"\n\n[exit code] {exit_code}"
    return header, body


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DRAGON recon CLI: choose tools, scan URL, save combined output.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--url", required=False, default=None, help="Target URL to scan.")
    parser.add_argument(
        "-t",
        "--tools",
        nargs="*",
        default=[],
        help="Tools to run. Supported: amaas, whatweb, nslookup, dig, nuclei, fuff, gobuster, nikto, dirbuster, httpx.",
    )
    parser.add_argument("-a", "--all", action="store_true", help="Run every supported tool automatically.")
    parser.add_argument("--dragon", action="store_true", help="Show the DRAGON banner and usage information.")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output file for combined results.")
    parser.add_argument("--gobuster-wordlist", default=DEFAULT_SUBDOMAIN_WORDLIST, help="Wordlist for gobuster subdomain scan.")
    parser.add_argument("--ffuf-wordlist", default=DEFAULT_WORDLIST, help="Wordlist for ffuf directory scan.")
    parser.add_argument("--dirbuster-wordlist", default=DEFAULT_WORDLIST, help="Wordlist for dirbuster.")
    parser.add_argument("--quiet", action="store_true", help="Only print summary and output file path.")
    return parser.parse_args()


def save_results(output_file: str, banner: str, tool_results: list[tuple[str, str]]) -> None:
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write(banner)
        out_file.write("\n\n")
        for header, body in tool_results:
            out_file.write(header)
            out_file.write("\n")
            out_file.write(body)
            out_file.write("\n\n")


def main() -> int:
    # enforce running as root immediately
    ensure_root()
    args = parse_arguments()

    # clear, show checking animation, install/update tools, then clear again
    try:
        os.system('clear')
    except Exception:
        pass
    first_run = is_first_run()
    display_checking()
    results = ensure_tools_installed(first_run=first_run)
    if first_run:
        mark_first_run_complete()
    # show results to the user before clearing the screen for the main banner
    display_check_results(results)
    try:
        os.system('clear')
    except Exception:
        pass

    # after checks, show the banner/help if requested
    if should_show_dragon_info():
        show_dragon_info()
        return 0

    # require URL for actual scans
    if not args.url:
        print(color_text("Error: target URL is required for scanning. Use -u/--url.", ANSI_RED), file=sys.stderr)
        return 1

    target_url = normalize_url(args.url)
    domain = normalize_domain(target_url)
    tools = [resolve_tool(tool) for tool in args.tools]

    if args.all:
        tools = list(TOOL_COMMANDS.keys())

    tools = order_tools(tools)

    if not tools:
        print(color_text("No tools selected. Use --all or -t TOOL1 TOOL2.", ANSI_RED), file=sys.stderr)
        return 1

    unsupported = [tool for tool in tools if tool not in TOOL_COMMANDS]
    if unsupported:
        print(color_text(f"Unsupported tool(s): {', '.join(unsupported)}", ANSI_RED), file=sys.stderr)
        return 1

    if not args.quiet:
        display_banner()
        print(color_text(f"Scanning target: {target_url}", ANSI_YELLOW))
        print(color_text(f"Saving output to: {args.output}\n", ANSI_GREEN))

    results = []
    for tool in tools:
        if not args.quiet:
            print(color_text(f"[RUNNING] {tool.upper()}...", ANSI_MAGENTA), flush=True)
        header, body = run_tool(tool, target_url, domain, args)
        results.append((header, body))
        if not args.quiet:
            if body.startswith("[WARNING]") or body.startswith("[ERROR]"):
                print(color_text(f"{tool.upper()}: {body}", ANSI_RED))
            else:
                print(color_text(f"[DONE] {tool.upper()}", ANSI_CYAN))

    save_results(args.output, ASCII_BANNER, results)
    print(color_text(f"Combined recon output written to: {args.output}", ANSI_GREEN))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print(color_text("[*] (Ctrl + C ) Detected, Trying To Exit ...", ANSI_YELLOW))
        print(color_text("[*] Stoping all services, Wait  ...", ANSI_YELLOW))
        print(color_text("[*] Thank You For Using Dragon =).", ANSI_GREEN))
        print(color_text("[*] Please consider supporting me :p", ANSI_MAGENTA))
        raise SystemExit(1)
