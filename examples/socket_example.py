import socket

def check_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("example.com", 80))
    s.close()
    print("Socket OK")

if __name__ == "__main__":
    check_socket()
