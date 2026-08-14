import Program

Backup_Themes = r"""# Theme styling
LOG_INFO = "\033[36m[ INFO ]\033[0m"       # Cyan [ INFO ]
LOG_SUCCESS = "\033[32m[ OK ]\033[0m" # Green [ OK ]
LOG_WARN = "\033[33m[ WARN ]\033[0m"       # Yellow [ WARN ]
LOG_ERROR = "\033[1;31m[ FAILED ]\033[0m"   # Bold Red [ Failed ]

COLOR_BLACK = "\033[30m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_LIGHTGRAY = "\033[37m"

COLOR_RESET = "\033[0m"
"""

# Themes fallback system
try:
    import Themes
    print(f"{Themes.LOG_SUCCESS} Loaded Themes.")
except ModuleNotFoundError:
    print("[-] Cannot find Themes File.\n running fallback system.")

    with open("Themes.py", 'w', encoding='utf-8') as TH:
        TH.write(Backup_Themes)
    del Backup_Themes # Clears The variable for freeing Memoryand preformance and also its now useless
    import Themes
    print(f"{Themes.LOG_SUCCESS} Loaded Themes (fallback recreated).")



def main():
    try:
        Program.EntryBoot()
    except (ModuleNotFoundError, ImportError, FileNotFoundError) as ex:
        raise ModuleNotFoundError(f"[ IMPORT ERROR ] {ex}")
    except Exception as e:
        raise Exception(f"[ UNEXPECTED ERROR ] {e}")

if __name__ == "__main__":
    main()