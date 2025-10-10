from datetime import datetime, timezone, timedelta
import sys
import config


ORANGE = "\033[38;5;214m"
RED = "\033[31m"
RESET = "\033[0m"
TZ = timezone(timedelta(hours=2))

# Only prints if -vv or more
def log(msg: str):
    if config.verbosity > 1:
        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"[{timestamp}] {msg}")


# Only prints if -v or more
def warn(msg: str):
    if config.verbosity > 0:
        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

        if sys.stdout.isatty():
            print(f"{ORANGE}[{timestamp}] [Warning] {msg}{RESET}")
        else:
            print(f"[{timestamp}] [Warning] {msg}")


# Always prints
def error(msg: str):
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

    if sys.stdout.isatty():
        print(f"{RED}[{timestamp}] [Error] {msg}{RESET}")
    else:
        print(f"[{timestamp}] [Error] {msg}")
