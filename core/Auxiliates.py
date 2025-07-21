import sys
from datetime import datetime

def pause():
    input("Pressione Enter para continuar...")
    sys.exit(0)

def message(msg):
    print(60 * "=")
    print(f"{msg}".upper())
    print(60 * "=")

def log_write(msg, file):
    file.write(f"{msg} - {datetime.now()}\n".upper())
    file.write(f"============================================================\n")
    