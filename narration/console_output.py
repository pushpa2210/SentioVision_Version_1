import os
import time

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def print_object_state(obj):
    """
    obj: dictionary with object state
    """

    print(f"ID          : {obj['id']}")
    print(f"Object      : {obj['object']}")
    print(f"Motion      : {obj['motion']}")
    print(f"Confidence  : {obj['confidence']}")
    print(f"Color       : {obj['color']}")
    print(f"Description : {obj['description']}")
    print("-" * 40)


def render_console(objects):
    """
    objects: list of object dictionaries
    """

    clear_console()
    print("SENTIVISION – OBJECT PERCEPTION OUTPUT\n")
    time.sleep(0.05)

    for obj in objects:
        print_object_state(obj)


from datetime import datetime

LOG_FILE = "logs/perception_log.txt"


def log_to_file(objects):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n===== FINAL PERCEPTION @ {timestamp} =====\n")


        for obj in objects:
            f.write(f"ID          : {obj['id']}\n")
            f.write(f"Object      : {obj['object']}\n")
            f.write(f"Motion      : {obj['motion']}\n")
            f.write(f"Confidence  : {obj['confidence']}\n")
            f.write(f"Color       : {obj['color']}\n")
            f.write(f"Description : {obj['description']}\n")
            f.write("-" * 40 + "\n")
