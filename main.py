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
        last = lines[-1].strip().split(" | ")
        name = last[0]
        timestamp = datetime.fromisoformat(last[1])
    return (name, timestamp)
    # pass


def add_visitor(visitor_name):
    last = get_last_visitor()
    if last and last[0].lower() == visitor_name.lower():
        raise DuplicateVisitorError("Can't sign in twice in a row!")
    # pass


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
