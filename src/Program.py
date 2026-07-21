#time Module
import time
# Dependenses
import requests as rq
import socket  
import os
import sys
from urllib.parse import urlparse
import webbrowser
import platform
os_name = platform.system()
#Themes Module for coloers and customization
try:
    import Themes as T
except FileNotFoundError:
    print("[!] Could not found the Themes File.")
    print("Please Import/Put the Theme file same directory as the program.")
    
try:
    import Systems.Tools.bruteforcer as Bruteforcer
except FileNotFoundError:
    print("[!] Could not found the Themes File.")
    print("Please Import/Put the Theme file same directory as the program.")


#--- NetVitals Program version 1.0---#
#- Open Source on Github.
if os_name == "Windows":
    os.system("title NetVitals v1.0")
elif os_name == "Linux" or os_name == "Darwin":
    os.system("""printf '\033]2;NetVitals v1.0\a'""")
else:
    pass

Default_wordlist = [
    "www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2", 
    "smtp", "vpn", "secure", "test", "dev", "api", "admin", "shop", 
    "cloud", "app", "staging", "ftp", "portal", "mysql", "m", "support", 
    "beta", "hosting", "vps", "email", "status", "cdn", "crm", "static", 
    "demo", "alpha", "git", "gitlab", "jira", "wiki", "docs", "forum", 
    "help", "analytics", "tools", "panel", "panel-admin", "manage", "manager", 
    "dashboard", "login", "signin", "auth", "oauth", "sso", "register", 
    "signup", "account", "accounts", "user", "users", "profile", "payment", 
    "billing", "invoice", "store", "cart", "checkout", "market", 
    "internal", "intranet", "corp", "office", "hr", "payroll", "staff", 
    "employee", "work", "local", "localhost", "db", "database", "sql", 
    "phpmyadmin", "backup", "backups", "archive", "storage", "files", 
    "download", "downloads", "media", "images", "img", "video", "assets", 
    "public", "private", "hidden", "secret"
]

Banner =  f"""
███╗   ██╗███████╗████████╗██╗   ██╗██╗████████╗ █████╗ ██╗     ███████╗
████╗  ██║██╔════╝╚══██╔══╝██║   ██║██║╚══██╔══╝██╔══██╗██║     ██╔════╝
██╔██╗ ██║█████╗     ██║   ██║   ██║██║   ██║   ███████║██║     ███████╗
██║╚██╗██║██╔══╝     ██║   ╚██╗ ██╔╝██║   ██║   ██╔══██║██║     ╚════██║
██║ ╚████║███████╗   ██║    ╚████╔╝ ██║   ██║   ██║  ██║███████╗███████║
╚═╝  ╚═══╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝"""
Menu = f"""
                ╭──────────────────────────────────╮
                |           NetVitals              |
                ╰──────────────────────────────────╯
    ╭────────────╯                  
    [1] Ip Lookup              [6] Coming Soon.
    [2] Url Lookup             [7] Coming Soon.
    [3] Sniffer                [8] Coming Soon.
    [4] Subdomain Enumerator   [9] Coming Soon.
    [5] Network BruteForcer    [10] Coming Soon.

                {T.COLOR_WHITE}by: BinaryAbyss Studios {T.COLOR_BLUE}
        [99] Exit    [01] More Options   [02] clear
{T.COLOR_RESET}"""
print(f"""
{Banner}
{Menu}
""")


def Clear_Console():
    if os_name == 'Windows':
        os.system('cls')
    elif os_name == 'Linux' or os_name == 'Darwin':
        os.system('clear')


def IpLookup(ip):
    if not ip:
        print(f"{T.LOG_ERROR} Invalid Ip (argument)")
    else:
        try:
            Response = rq.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            if Response.ok:
                print(f"{T.LOG_SUCCESS} Request Made")
                data = Response.json()
                print(f"{T.LOG_SUCCESS} Converted to a Json Response") 
            try:
                ip = data.get('ip', 'N/A')
                hostname = data.get('hostname', 'N/A')
                city = data.get('city', 'N/A')
                region = data.get('region', 'N/A')
                country = data.get('country', 'N/A')
                location = data.get('loc', 'N/A')
                org = data.get('org', 'N/A')
                postal = data.get('postal', 'N/A')
                timezone = data.get('timezone', 'N/A')
            except Exception as ex:
                print(f"{T.LOG_WARN} {ex}")

            Compressed_data = f"""
   {T.LOG_INFO}  Request Results
ip (internet protocol) = {ip}
hostname = {hostname}
city = {city}
region = {region}
country = {country}
location = {location}
org = {org}
postal = {postal}
timezone = {timezone}
"""
            print(Compressed_data)
        except Exception as ex:
            print(f"{T.LOG_ERROR} {ex}")


def UrlLookup(url):
    try:
        parased_url = urlparse(url)
        domain = parased_url.hostname
        if not domain:
            print(f"{T.LOG_ERROR} Could not parse a valid Domain From the url")
            return
        print(f"{T.LOG_SUCCESS} Resolving Domain: {domain}")

        ip_address = socket.gethostbyname(domain)
        print(f"{T.LOG_SUCCESS} ip Address: {ip_address}")
        IpLookup(ip_address)
    except Exception as ex:
        print(f"{T.LOG_ERROR} {ex}")

    
def sniffer():
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print(f"{T.LOG_SUCCESS} Sniffing network traffic... Press Ctrl+C to stop.")

        while True:
            raw_packet, address = sniffer.recvfrom(65565)
            print(f"Packet received from {address}: {raw_packet[:50]}") # Shows first 50 bytes
    except PermissionError:
         print(f"{T.LOG_ERROR} You must run this script with root/administrator privileges.")
         return
    except KeyboardInterrupt:
        print(f"\n{T.LOG_WARN} Packet Sniffing has been Stopped. KeyboardInterrupt")


def check_subdomains(target_domain, subdomain_list):
    """Tests a list of subdomains against a target domain with a progress bar."""
    print(f"\n[*] Starting scan on: {target_domain}")
    print(f"[*] Scanning {len(subdomain_list)} subdomains...\n")
    discovered = []
    total_subs = len(subdomain_list)

    for index, sub in enumerate(subdomain_list, start=1):
        full_url = f"{sub}.{target_domain}"

        # 1. Calculate progress percentage and bar width
        percent = int((index / total_subs) * 100)
        bar_length = 20
        filled_length = int(bar_length * index // total_subs)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        # 2. Print the progress bar (using \r to stay on the same line)
        sys.stdout.write(f"\rProgress: |{bar}| {percent}% ({index}/{total_subs})")
        sys.stdout.flush()

        try:
            ip_address = socket.gethostbyname(full_url)
            # 3. Clear the line temporarily to print the discovery neatly
            sys.stdout.write("\r" + " " * 60 + "\r")
            print(f"[+] Found: {full_url} -> {ip_address}")
            discovered.append(f"{full_url} -> {ip_address}")
        except socket.gaierror:
            pass

    # 4. Final cleanup line when done
    print(f"\n\n[+] Scan complete! Found {len(discovered)} active subdomains.")



def More_Options():
    Section = f"{T.COLOR_MAGENTA}[1]{T.COLOR_RESET} Visit Website {T.COLOR_MAGENTA}[2]{T.COLOR_RESET} Visit Source Code {T.COLOR_MAGENTA}[3]{T.COLOR_RESET} Return"
    print(Section)
    while True:
        choice = input("~> ")
        if choice == "1":
            webbrowser.open('https://binaryabyssstudios.github.io/')
        elif choice =="2":
            webbrowser.open('https://github.com/BinaryAbyssStudios/iplookup')
        elif choice =="3":
            return
        else:
            print(f"{T.LOG_ERROR} Invalid Input")

while True:
    try:
        cmd = input("~$ ")
    except KeyboardInterrupt:
        print(f"\n {T.LOG_INFO} Closing Program.") 
        time.sleep(0.5)
        sys.exit()
#Tools Commands.
    if cmd == "1":
        try:
            Target = input("Enter ip > ")
        except KeyboardInterrupt:
            print(f"\n {T.LOG_WARN} Closing Program.")
            time.sleep(0.5)
            sys.exit()
        IpLookup(Target)
    elif cmd == "2":
        try:
            Target = input("Enter Url > ")
        except KeyboardInterrupt:
            print(f"\n {T.LOG_WARN} Closing Program.")
            time.sleep(0.5)
            sys.exit()
        if not Target.startswith(('http://', 'https://')):
            Compressed_url = 'http://' + Target
            print(f"{T.LOG_INFO} Compressed Url: {Compressed_url}")
            UrlLookup(Compressed_url)
        else:
            UrlLookup(Target)
    elif cmd == "3":
        sniffer()
    elif cmd == "4":
        Target = input("Enter Target Domain> ").strip()
        WorldList_path = input("Enter Worldlist Full Path (leave it for default)").strip()
        if not WorldList_path:
            print("[*] Using default built-in wordlist...")
            check_subdomains(Target, Default_wordlist)
        elif os.path.exists(WorldList_path):
            try:
                with open(WorldList_path, "r", encoding="utf-8") as file:
                    wordlist = [line.strip() for line in file if line.strip()]

                print(f"[+] Successfully loaded {len(wordlist)} subdomains.")
                check_subdomains(Target, wordlist)
            except Exception as e:
                print(f"[-] Error reading file: {e}")
        else:
            print(f"[-] Error: The file path '{WorldList_path}' does not exist.")
    elif cmd == "5":
        try:
            Bruteforcer.Main()
        except Exception as e:
            print(f"{T.LOG_ERROR} A Error Has Accured.: {e}")

# Other nessesary Commands
    elif cmd == "02" or cmd == "clear":
        Clear_Console()
    elif cmd == "01":
        More_Options()
    elif cmd == "menu":
        print(f"""
{Banner}
{Menu}
""")
    elif cmd == "99":
        print(f"{T.LOG_INFO} Goodbye Friend.")
        time.sleep(1)
        sys.exit()
    else:
        print(f"{T.LOG_ERROR} Invaild Input")
