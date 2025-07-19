import threading

def worker():
    print("Worker thread running")

def start_threads():
    t = threading.Thread(target=worker)
    t.start()
    t.join()

if __name__ == "__main__":
    start_threads()
