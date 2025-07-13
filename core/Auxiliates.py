from datetime import datetime

def message(msg):
    print(f"{msg}".upper())
    print(60 * "=")

def log_write(msg, file):
    file.write(f"{msg} - {datetime.now()}\n".upper())
    file.write(f"============================================================\n")