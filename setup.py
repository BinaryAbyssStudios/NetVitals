import subprocess, sys, platform,os
print("[+] installing requirements..")


if os.path.isdir('.venv'):
    print("[ VIRTUAL ENVIRONMENT DETECTED ] There is an existing virtual environment.")
    venv_python = os.path.join('.venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join('.venv', 'bin', 'python')

else:
    print("[ NOT FOUND ] No virtual environment has been detected.")
    choice = input("Create virtual environment before installing? [Y/n]: ").strip().lower()

    if choice.startswith('n'):
        venv_python = sys.executable
    else:
        print("[+] creating virtual environment..")
        venv_result = subprocess.run(
            [sys.executable, '-m', 'venv', '.venv'],
            text=True,
            capture_output=True
        )
        print(venv_result.stderr)
        print(venv_result.stdout)

        venv_python = os.path.join('venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join('venv', 'bin', 'python')

print("[+] installing requirements into virtual environment..")
result = subprocess.run(
    [venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'],
    text=True,
    capture_output=True
)

print(result.stderr)
print(result.stdout)


os_name = platform.system()
prefix = "py" if os_name == "Windows" else "python3"


if result.returncode != 0:
    print(f"[ INSTALLING ERROR ] {result.stderr}")
else:
    print("[ INSTALL SUCCESS ]")
    print(f"[</> Reported Success] Requirements has been installing, Run  '{prefix} src/main.py' to continue")
