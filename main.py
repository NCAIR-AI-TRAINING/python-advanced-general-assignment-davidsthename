from datetime import datetime
import os


class DuplicateVisitorError(Exception):
    pass


class EarlyEntryError(Exception):
    pass


FILENAME = "visitors.txt"


def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            pass


def get_last_visitor():
    ensure_file()

    with open(FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()

        if not lines:
            return None
        last = lines[-1].strip().split(" - ", 1)
        timestamp_str = last[0]
        name = last[1]
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return (name, timestamp)
    # pass


def add_visitor(visitor_name):
    # last = get_last_visitor()
    # if last and last[0].lower() == visitor_name.lower():
    #     raise DuplicateVisitorError("Can't sign in twice in a row!")
    # # pass
    last = get_last_visitor()
    if last and last[0].lower() == visitor_name.lower():
        raise DuplicateVisitorError("Consecutive visitor detected!")
    if last:
        last_time = last[1]
        now = datetime.now()
        passed_seconds = (now - last_time).total_seconds()
        if passed_seconds < 300:
            raise EarlyEntryError(
                "Please wait at least 5 minutes before signing in again.")
    with open(FILENAME, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {visitor_name}\n")


def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
