import zipfile
import tarfile
import gzip

def compress_files():
    with zipfile.ZipFile("a.zip", "w") as z:
        z.write("json_example.py")
    with tarfile.open("b.tar.gz", "w:gz") as t:
        t.add("regex_example.py")

if __name__ == "__main__":
    compress_files()
    print("Compressed!")
