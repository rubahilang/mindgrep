import os
import subprocess
import shlex

def run_commands():
    os.system("echo 'Hello from os.system'")
    cmd = shlex.split("echo Hello from subprocess")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("subprocess:", result.stdout.strip())

if __name__ == "__main__":
    run_commands()
