import re

def find_pattern(s: str):
    if re.search(r"\d+", s):
        print("Found digits")
    new = re.sub(r"\s+", "-", s)
    print("Subbed:", new)

if __name__ == "__main__":
    find_pattern("This is 123 test")
