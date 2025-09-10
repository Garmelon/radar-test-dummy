#!/usr/bin/env python3

import os
import random
import string
import subprocess
import argparse

DIR = "dummy"
MAX_DEPTH = 6  # max directory nesting depth
os.makedirs(DIR, exist_ok=True)


def random_filename():
    return "".join(random.choices(string.ascii_lowercase, k=8)) + ".txt"


def random_dirname():
    return "".join(random.choices(string.ascii_lowercase, k=6))


def random_content():
    return (
        "".join(random.choices(string.ascii_letters + string.digits + " ", k=50)) + "\n"
    )


def depth(path):
    """Return relative depth of path inside DIR."""
    rel = os.path.relpath(path, DIR)
    if rel == ".":
        return 0
    return rel.count(os.sep) + 1


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


def create_directory_with_file():
    parent = pick_random_dir(DIR)
    if depth(parent) >= MAX_DEPTH:
        # too deep, just create a file instead
        create_file()
        return
    new_dir = os.path.join(parent, random_dirname())
    os.makedirs(new_dir, exist_ok=True)
    filepath = os.path.join(new_dir, random_filename())
    with open(filepath, "w") as f:
        f.write(random_content())
    print(f"Created directory and file: {filepath}")


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
    objects = [
        "file",
        "structure",
        "feature",
        "dummy",
        "logic",
        "data",
        "content",
        "directory",
    ]
    return f"{random.choice(verbs)} {random.choice(objects)}"


def git_commit():
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = random_commit_message()
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print(f"Committed with message: '{msg}'")
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")


def main(n_actions):
    actions = [create_file, delete_file, edit_file, create_directory_with_file]
    weights = [3, 1, 6, 2]  # edit > create > dir > delete

    for _ in range(n_actions):
        action = random.choices(actions, weights=weights, k=1)[0]
        action()

    git_commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", type=int, default=10, help="Number of actions before committing"
    )
    args = parser.parse_args()
    main(args.n)
