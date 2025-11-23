from datetime import datetime, timedelta
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
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return None
        last = lines[-1].strip().split(" | ")
        name = last[0]
        try:
            timestamp = datetime.fromisoformat(last[1])
        except ValueError:
            timestamp = None
    return (name, timestamp)


def add_visitor(visitor_name):
    # last = get_last_visitor()
    # if last and last[0].lower() == visitor_name.lower():
    #     raise DuplicateVisitorError("Can't sign in twice in a row!")
    # # pass
    last = get_last_visitor()
    if last and last[0].lower() == visitor_name.lower():
        raise DuplicateVisitorError("Can't sign in twice in a row!")

    if last:
        last_time = last[1]
        if datetime.now() - last_time < timedelta(minutes=5):
            raise EarlyEntryError("WAIT 5 MINUTES BEFORE SIGNING IN AGAIN!")

    timestamp = datetime.now().replace(microsecond=0).isoformat()
    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"{visitor_name} | {timestamp}\n")


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
