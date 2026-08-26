# generate_wordlist.py
# Generates password candidates and writes them to School_file_passwords.txt
# Edit the configuration near the top to match the patterns you want.

import itertools
from pathlib import Path
print("[+] Loading PasswordGenarator Program.")
# ---------- CONFIG ----------
General_OutPut_Path = "Genarated_Passowrd.txt"
output_path = Path(General_OutPut_Path)

# Base prefix(s) you want to try (examples from your message)
General_Prefix = None
prefixes = ["Example"]                     # try ["Example", "easy", "hard"] if you want variants

# Symbols that might appear after the prefix (from examples '@', '#', etc.)
symbols_after_prefix = ["@", "#", "$", "!"]  # edit to exactly what you want

# Digits: generate all 4-digit numbers 0000..9999 (change range if needed)
digit_length = 4
start_num = 0
end_num = 10**digit_length - 1  # inclusive

# Optional trailing symbols (example: HardPassowrd#2025! -> '!' is trailing)
trailing_symbols = ["", "!"]    # include "" to allow no trailing symbol

# Optional additional transformations:
# - include uppercase/lowercase prefix variants, or
# - add an extra separator like '-' or '_'
add_prefix_case_variants = False
additional_separators = [""]    # e.g. ["", "-"] to add optional separator between prefix and symbol/digits

max_allowed_combinations = 5_000_000  # set a reasonable safety cap

# ---------- END CONFIG ----------

def generate_prefix_variants(prefix_list, case_variants):
    if not case_variants:
        return prefix_list
    out = []
    for p in prefix_list:
        out.extend({p, p.lower(), p.upper(), p.capitalize()})
    # remove duplicates while preserving order-ish
    return list(dict.fromkeys(out))

def estimate_total(prefixes_count, symbols_count, range_count, trailing_count, separators_count):
    return prefixes_count * symbols_count * range_count * trailing_count * separators_count

def Password_Genearator_Mains():
    prefixes_use = generate_prefix_variants(prefixes, add_prefix_case_variants)
    range_count = end_num - start_num + 1
    total = estimate_total(
        len(prefixes_use),
        len(symbols_after_prefix),
        range_count,
        len(trailing_symbols),
        len(additional_separators)
    )

    print(f"Estimated combinations: {total:,}")
    if total > max_allowed_combinations:
        print("ERROR: estimated combination count exceeds safety cap.")
        print("Either narrow your charset/length or increase max_allowed_combinations in the script.")
        return

    # Confirm overwrite
    if output_path.exists():
        print(f"Overwriting existing file: {output_path}")
    else:
        print(f"Creating file: {output_path}")

    with output_path.open("w", encoding="utf-8") as f:
        # iterate
        for prefix in prefixes_use:
            for sep in additional_separators:
                for sym in symbols_after_prefix:
                    for num in range(start_num, end_num + 1):
                        num_str = str(num).zfill(digit_length)
                        for trail in trailing_symbols:
                            pw = f"{prefix}{sep}{sym}{num_str}{trail}"
                            f.write(pw + "\n")
    print("Done. File written:", output_path)
    print(f"Final count written (approx): {total:,}")

def Menu():
    return f"""
[1] Change Prefix {prefixes}
[2] Change Sympoles {symbols_after_prefix}
[3] Change Digit Length (Default = 4) {digit_length}
[4] Change Max Allowed Combinations (Default = 5M [5_000_000] )
[5] Change Output Path + File Name ({General_OutPut_Path})

     [6] Exit Program

[00] Start Genarating
""" 

def Handle_Prefix():
    print(f"Avaliable Prefix: {len(prefixes)}")
    if len(prefixes) < 1:
        print("No Current Prefixes to Display")
    else:
        print(f"Prefixes: {prefixes}") 
        Temp_Menu = "[1] Change prefix, [2] Add Prefix, [3] Remove Prefix, [4] Return"
        print(Temp_Menu)
    while True:
        try:
            user_HandlePrefix_input = input("Enter Options~$ ")
            if user_HandlePrefix_input == '1':
                Change_prefix = input("Enter a prefix to Change~$ ").replace(" ", "") # Removing Spaces to Free up Size and Make Password Genarating Much Easier , Passwords Normally Dosent Contain Spaces
                Replacment_Prefix = input("Enter a Replacment Prefix~$ ").replace(" ", "")
                if Change_prefix not in prefixes:
                    print(f"The Prefix: {Change_prefix} Dosent Exist to Replace")
                    return
                else:
                    prefixes.remove(Change_prefix)
                    print(f"[+] {Change_prefix} Has Been Removed.")
                    prefixes.extend(Replacment_Prefix)
                    print(f"[+] {Replacment_Prefix} Has Been Added.")
                    return

            elif user_HandlePrefix_input == '2':
                Add_Prefix_Input = input("Enter a Prefix to add~$ ").replace(" ", "")
                if not Add_Prefix_Input:
                    print("[-] Please Enter a vaild Prefix to Add.")
                prefixes.append(Add_Prefix_Input)
                print(f"[+] Prefix Has been Added: {Add_Prefix_Input}")

            elif user_HandlePrefix_input == '3':
                Remove_Prefix_Input = input("Enter a Prefix to Remove~$ ").replace(" ", "")
                if not Remove_Prefix_Input:
                    print("[-] Please Enter a vaild Prefix to Remove.")
                else:
                    prefixes.remove(Remove_Prefix_Input)
            elif user_HandlePrefix_input == '4':
                return
            
        except KeyboardInterrupt:
            print("CTRl, C, Exiting Prefixes Manager.")
            return
        except Exception as e:
            print(f"[-] a Critical Error has Occured: {e}")

def Handle_Symboles():
    print(f"Avaliable symbols: {len(symbols_after_prefix)}")
    if len(prefixes) < 1:
        print("No Current sympoles to Display")
    else:
        print(f"Prefixes: {symbols_after_prefix}") 
        Temp_Menu = "[1] Change symbol, [2] Add symbol, [3] Remove sympol, [4] Return"
        print(Temp_Menu)
    while True:
        try:
            user_HandleSymbol_input = input("Enter Options~$ ")
            if user_HandleSymbol_input == '1':
                Change_symbol = input("Enter a sympol to Change~$ ").replace(" ", "") # Removing Spaces to Free up Size and Make Password Genarating Much Easier , Passwords Normally Dosent Contain Spaces
                Replacment_symbol = input("Enter a Replacment symbol~$ ").replace(" ", "")
                if Change_symbol not in symbols_after_prefix:
                    print(f"The Prefix: {Change_symbol} Dosent Exist to Replace")
                    return
                else:
                    prefixes.remove(Change_symbol)
                    print(f"[+] {Change_symbol} Has Been Removed.")
                    prefixes.append(Replacment_symbol)
                    print(f"[+] {Replacment_symbol} Has Been Added.")
                    return

            elif user_HandleSymbol_input == '2':
                Add_Symbol_Input = input("Enter a Symbol to add~$ ").replace(" ", "")
                if not Add_Symbol_Input:
                    print("[-] Please Enter a vaild Symbol to Add.")
                symbols_after_prefix.append(Add_Symbol_Input)
                print(f"[+] Sympol has been Added: {Add_Symbol_Input}")

            elif user_HandleSymbol_input == '3':
                Remove_Symbol_Input = input("Enter a Symbol to Remove~$ ").replace(" ", "")
                if not Remove_Symbol_Input:
                    print("[-] Please Enter a vaild Symbol to Remove.")
                else:
                    symbols_after_prefix.remove(Remove_Symbol_Input)
            elif user_HandleSymbol_input == '4':
                return
            
        except KeyboardInterrupt:
            print("CTRl, C, Exiting Symbols Manager.")
            return
        except Exception as e:
            print(f"[-] a Critical Error has Occured: {e}")

def Handle_Digit_Length():
    global digit_length

    print(f"Current Digit Limit: {digit_length}")
    handle_digit_input = input("Enter a new Digit Limit: ")
    print(f"[+] Changing Digit length by {handle_digit_input}")
    digit_length = handle_digit_input 
    print(f"[+] Task Finished Successfully.")
    print(Menu())
    return

def Handle_Max_Allowed_Combinations():
    global max_allowed_combinations

    print(f"Current Digit Limit: {max_allowed_combinations}")
    print("[!] For every 3 Digit put an underScore '_' ")
    handle_max_allowed_input = input("Enter new Max Allowed Combination: ").replace(" ", "")
    print("[+] Changing Max Allowed Combinations")
    max_allowed_combinations = handle_max_allowed_input
    print(f"[+] Task Finished Successfully.")
    print(Menu())
    return

def Handle_Output_File():
    global General_OutPut_Path

    print(f"Current File Name/Path: {General_OutPut_Path}")
    print("[1] Change File Name, [2] Change Path")
    while True:
        Handle_output_Userinput = input("Enter a Choice~$ ")
        if Handle_output_Userinput == '1':
            New_File_Name = input("Enter a new File Output Name: ").replace(" ", "_").replace("/", "").replace("\\", "")
            if not New_File_Name:
                print("[-] Please Enter a Vaild input")
            else:
                print("[+] Changing Output Name")
                General_OutPut_Path = New_File_Name
                print("[+] Task Finished successfully.")
                print(f"[+] New Name: {General_OutPut_Path}")
                print(Menu())
                return
            
        elif Handle_output_Userinput == '2':
            New_Path = input("Enter a New File Output Path: ").replace(" ", "")
            Temp_Variable = General_OutPut_Path
            print("[+] Changing Output Path")
            General_OutPut_Path =  f"{New_Path}{Temp_Variable}"
            print("[+] Task Finished successfully.")
            print(f"[+] New Path: {General_OutPut_Path}")
            print(Menu())
            return

def main():
    print(Menu())
    while True:
        try: 
            User_input_choice = input("Paswowrd Genarator~$ ")
            if User_input_choice in ['1', '2', '3', '4', '5', '6', '00', 'Menu', 'menu', 'MENU']:
                if User_input_choice == '1':
                    Handle_Prefix()
                elif User_input_choice == '2':
                    Handle_Symboles()
                elif User_input_choice == '3':
                    Handle_Digit_Length()
                elif User_input_choice == '4':
                    Handle_Max_Allowed_Combinations()
                elif User_input_choice == '5':
                    Handle_Output_File()
                elif User_input_choice == '6':
                    return
                elif User_input_choice == '00':
                    Password_Genearator_Mains()
                elif User_input_choice in ['Menu', 'menu', 'MENU']:
                    print(Menu())
            else:
                print("[-] Invaild User INPUT.")
        except KeyboardInterrupt:
            print("\n CTRl, C, Exiting Program.")
            return
        except Exception as e:
            print(f"\n [-] a Critical Error has Occured: {e}")

if __name__ == "__main__":
    main()