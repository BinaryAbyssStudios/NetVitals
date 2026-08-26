#!/usr/bin/env python3
"""
nmap_tool.py - Simplified menu-driven nmap wrapper.

Pick a scan type from the menu, then enter a target IP/range or just
press Enter to use an auto-detected default (your local subnet or gateway).

Requires: nmap installed on the system (sudo apt install nmap)
Note: some scans (SYN, OS detection, UDP) need root -> run with sudo.
"""

import ipaddress
import os
import platform
import re
import shutil
import subprocess
import sys

if shutil.which("nmap") is None:
    print("[-] nmap  not found. This Program requires nmap.")
    sys.exit() 
print("[+] Found nmap Package")

OS_NAME = platform.system()  # "Linux", "Darwin" (macOS), or "Windows"


def netmask_to_cidr(netmask):
    """Convert a dotted netmask like 255.255.255.0 to a prefix length like 24."""
    try:
        return sum(bin(int(octet)).count("1") for octet in netmask.split("."))
    except Exception:
        return None

# Scan definitions: key -> (label, nmap_args, target_type)
# target_type: "subnet" -> default target is your local subnet (for range scans)
#              "host"   -> default target is your default gateway (for single-host scans)
SCANS = {
    "1": ("Ping scan (host discovery)",              ["-sn"], "subnet"),
    "2": ("Quick scan (top 100 ports)",               ["-F"],  "host"),
    "3": ("Full port scan (all 65535 ports)",         ["-p-"], "host"),
    "4": ("Service version detection",                ["-sV"], "host"),
    "5": ("OS detection (needs root)",                ["-O"],  "host"),
    "6": ("Aggressive scan (OS + version + scripts)", ["-A"],  "host"),
    "7": ("SYN scan - stealthy (needs root)",         ["-sS"], "host"),
    "8": ("UDP scan",                                 ["-sU"], "host"),
}

ROOT_REQUIRED_FLAGS = {"-sS", "-O", "-sU", "-A"}


def check_nmap_installed():
    if shutil.which("nmap") is None:
        print("[!] nmap is not installed. Install it with: sudo apt install nmap")
        sys.exit(1)


def is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0


def run_cmd(cmd):
    """Run a command and return its stdout as text, or None on failure."""
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return None


def get_default_subnet():
    """Detect the local subnet (e.g. 10.10.0.0/18), OS-specific."""
    try:
        if OS_NAME == "Linux":
            output = run_cmd(["ip", "route"])
            if output:
                for line in output.splitlines():
                    parts = line.split()
                    if parts and "/" in parts[0] and "scope" in line and "link" in line:
                        return parts[0]

        elif OS_NAME == "Darwin":  # macOS
            output = run_cmd(["ifconfig"])
            if output:
                # look for the first active interface with both an inet addr and netmask
                ip_match = re.search(r"inet (\d+\.\d+\.\d+\.\d+) netmask (0x[0-9a-fA-F]+)", output)
                if ip_match:
                    ip_addr, hexmask = ip_match.groups()
                    prefix = bin(int(hexmask, 16)).count("1")
                    network = ipaddress.ip_network(f"{ip_addr}/{prefix}", strict=False)
                    return str(network)

        elif OS_NAME == "Windows":
            output = run_cmd(["ipconfig"])
            if output:
                ip_match = re.search(r"IPv4 Address[.\s]*: (\d+\.\d+\.\d+\.\d+)", output)
                mask_match = re.search(r"Subnet Mask[.\s]*: (\d+\.\d+\.\d+\.\d+)", output)
                if ip_match and mask_match:
                    prefix = netmask_to_cidr(mask_match.group(1))
                    if prefix is not None:
                        network = ipaddress.ip_network(f"{ip_match.group(1)}/{prefix}", strict=False)
                        return str(network)
    except Exception:
        pass

    return "192.168.1.0/24"  # fallback if detection fails on any platform


def get_default_gateway():
    """Detect the default gateway/router IP, OS-specific."""
    try:
        if OS_NAME == "Linux":
            output = run_cmd(["ip", "route"])
            if output:
                for line in output.splitlines():
                    if line.startswith("default"):
                        parts = line.split()
                        if "via" in parts:
                            return parts[parts.index("via") + 1]

        elif OS_NAME == "Darwin":  # macOS
            output = run_cmd(["route", "-n", "get", "default"])
            if output:
                match = re.search(r"gateway: (\d+\.\d+\.\d+\.\d+)", output)
                if match:
                    return match.group(1)

        elif OS_NAME == "Windows":
            output = run_cmd(["ipconfig"])
            if output:
                match = re.search(r"Default Gateway[.\s]*: (\d+\.\d+\.\d+\.\d+)", output)
                if match:
                    return match.group(1)
    except Exception:
        pass

    return None


def prompt_target(default):
    target = input(f"Target IP/range [Enter for default: {default}]: ").strip()
    return target if target else default


def maybe_warn_root(args):
    if any(flag in ROOT_REQUIRED_FLAGS for flag in args) and not is_root():
        print("[!] This scan usually needs root. Re-run the script with sudo if it fails or hangs.")


def run_scan(args, target):
    cmd = ["nmap"] + args + [target]
    print(f"\n[+] Running: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted.")
    except Exception as e:
        print(f"[!] Error running nmap: {e}")


def print_menu():
    print("\n=== Simple Nmap Tool ===")
    for key, (label, _, _) in SCANS.items():
        print(f"{key}. {label}")
    print("0. Exit")


def main():
    check_nmap_installed()
    default_subnet = get_default_subnet()
    default_gateway = get_default_gateway() or default_subnet

    print("Only scan networks/devices you own or have permission to scan.")

    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("Bye.")
            break

        if choice not in SCANS:
            print("[!] Invalid option, try again.")
            continue

        label, args, target_type = SCANS[choice]
        default_target = default_subnet if target_type == "subnet" else default_gateway

        target = prompt_target(default_target)
        maybe_warn_root(args)
        run_scan(args, target)


if __name__ == "__main__":
    main()