import logging
import sys
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from fix_tox.testing import add_missing_test_functions


def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
    add_missing_test_functions(event.src_path)

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


def watch(root_dir):
    observer = Observer()

    patterns = ["*.py"]


    ignore_patterns = ['flycheck*', '.#*']
    ignore_directories = ['.tox', '.git', './tests']
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    observer.schedule(event_handler, root_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
