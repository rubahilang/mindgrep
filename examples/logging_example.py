import logging

logging.basicConfig(level=logging.INFO)

def log_something():
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error!")
    print("Also a print()")

if __name__ == "__main__":
    log_something()
