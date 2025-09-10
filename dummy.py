#!/usr/bin/env python3

import os
import random
import string
import subprocess

DIR = "dummy"
os.makedirs(DIR, exist_ok=True)


def random_filename():
    return "".join(random.choices(string.ascii_lowercase, k=8)) + ".txt"


def random_content():
    return (
        "".join(random.choices(string.ascii_letters + string.digits + " ", k=50)) + "\n"
    )


def pick_random_dir(base_dir):
    """Pick a random directory (recursively) inside base_dir, including base_dir itself."""
    dirs = [base_dir]
    for root, subdirs, _ in os.walk(base_dir):
        for d in subdirs:
            dirs.append(os.path.join(root, d))
    return random.choice(dirs)


def create_file():
    target_dir = pick_random_dir(DIR)
    os.makedirs(target_dir, exist_ok=True)
    filename = random_filename()
    filepath = os.path.join(target_dir, filename)
    with open(filepath, "w") as f:
        f.write(random_content())
    print(f"Created: {filepath}")


def delete_file():
    files = []
    for root, _, filenames in os.walk(DIR):
        for f in filenames:
            files.append(os.path.join(root, f))
    if not files:
        return
    file_to_delete = random.choice(files)
    os.remove(file_to_delete)
    print(f"Deleted: {file_to_delete}")


def edit_file():
    files = []
    for root, _, filenames in os.walk(DIR):
        for f in filenames:
            files.append(os.path.join(root, f))
    if not files:
        return
    file_to_edit = random.choice(files)
    with open(file_to_edit, "a") as f:
        f.write(random_content())
    print(f"Edited: {file_to_edit}")


def random_commit_message():
    verbs = [
        "Update",
        "Fix",
        "Refactor",
        "Remove",
        "Improve",
        "Add",
        "Modify",
        "Change",
    ]
    objects = ["file", "structure", "feature", "dummy", "logic", "data", "content"]
    return f"{random.choice(verbs)} {random.choice(objects)}"


def git_commit():
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = random_commit_message()
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print(f"Committed with message: '{msg}'")
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")


# Weighted action selection
actions = [create_file, delete_file, edit_file]
weights = [3, 1, 6]  # edit > create > delete

if __name__ == "__main__":
    action = random.choices(actions, weights=weights, k=1)[0]
    action()
    git_commit()
