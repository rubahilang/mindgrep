import os
import shutil
from pathlib import Path

def file_ops():
    Path("temp.txt").write_text("hello world")
    print(Path("temp.txt").read_text())
    shutil.copy("temp.txt", "temp_copy.txt")
    os.rename("temp_copy.txt", "renamed.txt")
    os.remove("temp.txt")
    os.remove("renamed.txt")

if __name__ == "__main__":
    file_ops()
