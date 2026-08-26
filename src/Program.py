#── Time Module ────────────────
import time
# Dependenses
import socket  
import os
import sys
from urllib.parse import urlparse
import webbrowser
import platform
import json
from datetime import datetime
os_name = platform.system()
try: 
    import Themes as T # Themes Module for coloers and customization
    import Systems.Tools.bruteforcer as Bruteforcer
    import Systems.Tools.passwordGenarator as PW
    import Systems.Tools.deauth_Attack as da_attack
    import Systems.Tools.Nmap_tool as NTool
    import Systems.Tools.Arp_spoof as ASP
except ModuleNotFoundError: 
    print("[!] Could not found Some Essensials Files File.")
    print("Please Import/Put the Theme file same directory as the program.")

# ── Free up Ram usage and optimization ────────────────────
del Bruteforcer, PW, da_attack, NTool, ASP
del sys.modules["Systems.Tools.bruteforcer"]
del sys.modules["Systems.Tools.passwordGenarator"]
del sys.modules["Systems.Tools.deauth_Attack"]
del sys.modules["Systems.Tools.Nmap_tool"]
del sys.modules["Systems.Tools.Arp_spoof"]

# ── Saftey Check ────────────────
try:
    import requests as rq
    import whois
    if os_name == 'Windows':
        import pywifi
        del pywifi
    else:
        pass    
except (ModuleNotFoundError, ImportError) as e:
    raise Exception(f"{T.LOG_ERROR} Could not found essensials modules, Please Install it from requirements.txt: {e}")

# ── NetVitals Program version 1.5 ───────────────────────────────────
#- Open Source on Github.
if os_name == "Windows":
    os.system("title NetVitals v1.5")
elif os_name == "Linux" or os_name == "Darwin":
    os.system("""printf '\033]2;NetVitals v1.5\a'""")
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

Banner =  r"""
███╗   ██╗███████╗████████╗██╗   ██╗██╗████████╗ █████╗ ██╗     ███████╗
████╗  ██║██╔════╝╚══██╔══╝██║   ██║██║╚══██╔══╝██╔══██╗██║     ██╔════╝
██╔██╗ ██║█████╗     ██║   ██║   ██║██║   ██║   ███████║██║     ███████╗
██║╚██╗██║██╔══╝     ██║   ╚██╗ ██╔╝██║   ██║   ██╔══██║██║     ╚════██║
██║ ╚████║███████╗   ██║    ╚████╔╝ ██║   ██║   ██║  ██║███████╗███████║
╚═╝  ╚═══╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝"""
def Menu():
    return f"""                         
  ╭─────────────────╮         ╭────────────────────╮
  |Network Discovery| --</>-- | Network Essensials |
  ╰─────────────────╯         ╰────────────────────╯
                
    [1] Ip Lookup              [6] Network BruteForcer.
    [2] Url Lookup             [7] Password Genarator.
    [3] Whois Lookup           [8] Deauth Attack.
    [4] Sniffer                [9] Nmap Simplified.
    [5] Subdomain Enumerator   [10] Arp Spoof.

             {T.COLOR_LIGHTGRAY}by: BinaryAbyss Studios, LLC {T.COLOR_BLUE} 
        [99] Exit    [01] More Options   [02] clear {T.COLOR_RESET}"""


def Clear_Console():
    if os_name == 'Windows':
        os.system('cls')
    elif os_name in ['Linux', 'Darwin']:
        os.system('clear')


def IpLookup(ip):
    if not ip:
        print(f"{T.LOG_ERROR} Invalid Ip (argument)")
    else:
        try:
            Response = rq.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            if Response.ok:
                print(f"{T.LOG_SUCCESS} Request Made.")
                data = Response.json()
                print(f"{T.LOG_SUCCESS} Converted to a Json Response.") 
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

def clean_value(v):
    """Flatten lists to first item, convert dates to strings"""
    print(f"{T.LOG_SUCCESS} Flattering {v}")
    if isinstance(v, list):
        v = v[0] if v else None
    if isinstance(v, datetime):
        v = v.strftime("%Y-%m-%d %H:%M:%S")
    return v


def whois_lookup(domain):
    w = whois.whois(domain)
    print(f"{T.LOG_SUCCESS} Request Made.")
    if not w.domain_name:
        return {f"{T.LOG_WARN} No WHOIS data found for this domain"}

    result = {
        "domain_name": clean_value(w.domain_name),
        "registrar": clean_value(w.registrar),
        "creation_date": clean_value(w.creation_date),
        "expiration_date": clean_value(w.expiration_date),
        "updated_date": clean_value(w.updated_date),
        "name_servers": w.name_servers if isinstance(w.name_servers, list) else [w.name_servers],
        "status": w.status if isinstance(w.status, list) else [w.status],
        "country": clean_value(getattr(w, "country", None)),
        "org": clean_value(getattr(w, "org", None)),
    }
    return result

    
def sniffer():
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print(f"{T.LOG_SUCCESS} Sniffing network traffic... Press Ctrl+C to stop.")

        while True:
            raw_packet, address = sniffer.recvfrom(65565)
            print(f"Packet received from {address}: {raw_packet[:200]}") # Shows first 200 bytes
    except PermissionError:
         print(f"{T.LOG_ERROR} You must run this script with root/administrator privileges.")
         return
    except KeyboardInterrupt:
        print(f"\n{T.LOG_WARN} Packet Sniffing has been Stopped. KeyboardInterrupt")


def check_subdomains(target_domain, subdomain_list):
    """Tests a list of subdomains against a target domain with a progress bar."""
    print(f"\n[*] Starting scan on: {target_domain}")
    print(f"{T.LOG_SUCCESS} Scanning {len(subdomain_list)} subdomains...\n")
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
            print(f"{T.LOG_INFO} Found: {full_url} -> {ip_address}")
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
            webbrowser.open('https://github.com/BinaryAbyssStudios/NetVitals')
        elif choice =="3":
            return
        else:
            print(f"{T.LOG_ERROR} Invalid Input")
            

def EntryBoot():
    print(f"""
{Banner}
{Menu()}
""")
    while True:
        try:
            cmd = input("~$ ").strip().lower()
        #Tools Commands.
            if cmd == "1":
                Target = input("Enter ip > ").strip()
                IpLookup(Target)
            elif cmd == "2":
                Target = input("Enter Url > ").strip()
                if not Target.startswith(('http://', 'https://')):
                    Compressed_url = 'http://' + Target
                    print(f"{T.LOG_INFO} Compressed Url: {Compressed_url}")
                    UrlLookup(Compressed_url)
                else:
                    UrlLookup(Target)
            elif cmd == "3":
                while True:
                    Target = input("Enter Target Domain> ").strip()
                    if not Target:
                        print(f"{T.LOG_WARN} Enter a vaild domain.")
                        print(f"{T.LOG_INFO} Exiting")
                        break
                    else:
                        result = whois_lookup(Target)
                        print(json.dumps(result, indent=2))
                        break
            elif cmd == "4":
                sniffer()
            elif cmd == "5":
                Target = input("Enter Target Domain> ").strip()
                WorldList_path = input("Enter Worldlist Full Path (leave it for default)").strip()
                if not WorldList_path:
                    print(f"{T.LOG_INFO} Using default built-in wordlist...")
                    check_subdomains(Target, Default_wordlist)
                elif os.path.exists(WorldList_path):
                    try:
                        with open(WorldList_path, "r", encoding="utf-8") as file:
                            wordlist = [line.strip() for line in file if line.strip()]

                        print(f"{T.LOG_SUCCESS} Successfully loaded {len(wordlist)} subdomains.")
                        check_subdomains(Target, wordlist)
                    except Exception as e:
                        print(f"{T.LOG_ERROR} Error reading file: {e}")
                else:
                    print(f"{T.LOG_ERROR} The file path '{WorldList_path}' does not exist.")

            elif cmd == "6":
                print(f"{T.LOG_INFO} Running Script.")
                import Systems.Tools.bruteforcer as Bruteforcer
                Bruteforcer.main()
                del Bruteforcer
                del sys.modules["Systems.Tools.bruteforcer"]
            elif cmd == "7":
                print(f"{T.LOG_INFO} Running Script.")
                import Systems.Tools.passwordGenarator as PW
                PW.main()
                del PW
                del sys.modules["Systems.Tools.passwordGenarator"]
            elif cmd == "8":
                if os_name == 'Linux':
                    import Systems.Tools.deauth_Attack as da_attack
                    da_attack.main()
                    del da_attack
                    del sys.modules["Systems.Tools.deauth_Attack"]
                else:
                    print(f"{T.LOG_WARN} this script only supports GNU/Linux os (operating System)")
            elif cmd == "9":
                print(f"{T.LOG_INFO} Running Script.")
                import Systems.Tools.Nmap_tool as NTool
                NTool.main()
                del NTool
                del sys.modules["Systems.Tools.Nmap_tool"]
            elif cmd == "10":
                if os_name == 'Linux':
                    import Systems.Tools.Arp_spoof as ASP
                    ASP.main()
                    del ASP
                    del sys.modules["Systems.Tools.Arp_spoof"]
                else:
                    print(f"{T.LOG_WARN} this script only supports GNU/Linux os (operating System)")
        # Other nessesary Commands
            elif cmd == "02" or cmd == "clear":
                Clear_Console()
            elif cmd == "01":
                More_Options()
            elif cmd  in ['menu']:
                print(f"""
        {Banner}
        {Menu()}
        """)
            elif cmd == "99":
                print(f"{T.LOG_INFO} Goodbye.")
                sys.exit()
            else:
                print(f"{T.LOG_ERROR} Invaild Input")
        except KeyboardInterrupt:
            sys.exit(f"\n{T.LOG_INFO} CTRL C , KeyboardInterrupt , Closing Program.")
        except ValueError as e:
            print(f"{T.LOG_ERROR} Value Error: {e}")
        except Exception as e:
            print(f"{T.LOG_ERROR} Critical Error has Occured : {e}")
