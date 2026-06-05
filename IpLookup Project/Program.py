#time Module
import time
# Dependenses
import requests as rq
import socket  
import os
import sys
from urllib.parse import urlparse
import webbrowser
#Themes Module for coloers and customization
import Themes as T


#--- IPLOOKUP Program version 1.0---#
#- Open Source on Github.

os.system("title IPLookup v1.0")
Banner =  """
██╗██████╗ ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ 
██║██╔══██╗██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
██║██████╔╝██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
██║██╔═══╝ ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ 
██║██║     ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     
╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                            
"""
Menu = f"""{T.COLOR_RED} [1] {T.COLOR_RESET} Ip lookup {T.COLOR_RED} [2] {T.COLOR_RESET} Url lookup
{T.COLOR_RED} [3] {T.COLOR_RESET} More Options \n 
{T.COLOR_LIGHTGRAY}[4]{T.COLOR_RESET} Exit \n"""
print(Banner)
print(Menu)


def IpLookup(ip):
    if not ip:
        print(f"{T.LOG_ERROR} Invaild Ip (argument)")
    else:
        try:
            Response = rq.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            if Response.ok:
                print(f"{T.LOG_SUCCESS} Request Made")
                data = Response.json()
                print(f"{T.LOG_SUCCESS} Converted to a Json Response") 
            try:
                ip = data['ip']
                hostname = data['hostname']
                city = data['city']
                region = data['region']
                country = data['country']
                location = data['loc']
                org = data['org']
                postal = data['postal']
                timezone = data['timezone']
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
            print(f"{T.LOG_ERROR} Could not parse a vaild Domain From the url")
            return
        print(f"{T.LOG_SUCCESS} Resolving Domain: {domain}")

        ip_address = socket.gethostbyname(domain)
        print(f"{T.LOG_SUCCESS} ip Address: {ip_address}")
        IpLookup(ip_address)
    except Exception as ex:
        print(f"{T.LOG_ERROR} {ex}")

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
            print(f"{T.LOG_ERROR} Invaild Input")

while True:
    try:
        cmd = input("> ")
    except KeyboardInterrupt:
        print(f"{T.LOG_WARN} Closing Program.") 
        time.sleep(0.5)
        sys.exit()
    if cmd == "1":
        Target = input("Enter ip > ")
        IpLookup(Target)
    elif cmd == "2":
        Target = input("Enter Url > ")
        if not Target.startswith(('http://', 'https://')):
            Compressed_url = 'http://' + Target
            print(f"{T.LOG_INFO} Compressed Url: {Compressed_url}")
            UrlLookup(Compressed_url)
        else:
            UrlLookup(Target)
    elif cmd == "3":
        More_Options()
    elif cmd == "4":
        print(f"{T.LOG_INFO} Goodboy Friend.")
        time.sleep(1)
        sys.exit()
    else:
        print(f"{T.LOG_ERROR} Invaild Input")