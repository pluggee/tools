#!/Users/sherifeid/.pyenv/py312/bin/python3

""" This script analyzes the current directory and reports folder sizes """

import os
import sys
from humanize import naturalsize
from itertools import cycle
import argparse

def parse_human_readable_size(size_str):
    """Convert human-readable size strings (e.g., 1G, 200M, 1T) to bytes."""
    units = {"B": 1, "K": 10**3, "M": 10**6, "G": 10**9, "T": 10**12}
    size_str = size_str.upper().strip()
    unit = size_str[-1]

    if unit.isdigit():  # If no unit is given, assume bytes
        return int(size_str)

    if unit in units:
        return int(float(size_str[:-1]) * units[unit])
    else:
        raise ValueError(f"Invalid size unit '{unit}' in '{size_str}'")

def get_directory_size(directory):
    """Recursively calculate directory size in bytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def main(min_size_bytes=None):
    current_directory = os.getcwd()
    dir_sizes = []

    # Start displaying progress
    print(f"{'Directory':<40} {'Size':>10}")
    print("-" * 52)

    # Progress spinner
    spinner = cycle(["|", "/", "-", "\\"])  

    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path):
            # Update spinner
            sys.stdout.write(f"\rProcessing {item:<30} {next(spinner)}")
            sys.stdout.flush()

            size = get_directory_size(item_path)
            if min_size_bytes is None or size >= min_size_bytes:
                dir_sizes.append((item, size))
                print(f"\r{item:<40} {naturalsize(size):>10}")

    # Sort and display final list
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    
    print("\nSummary (Sorted by size):")
    for directory, size in dir_sizes:
        print(f"{directory:<40} {naturalsize(size):>10}")

    # Print total size of displayed directories
    total_size = sum(size for _, size in dir_sizes)
    print("-" * 52)
    print(f"{'Total size of displayed directories:':<40} {naturalsize(total_size):>10}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report directory sizes with optional size filtering.")
    parser.add_argument(
        "min_size",
        nargs="?",
        default=None,
        help="Minimum size filter in human-readable format (e.g., 1G, 200M, 1T)."
    )
    args = parser.parse_args()

    # Parse the human-readable size argument if provided
    min_size_bytes = None
    if args.min_size:
        try:
            min_size_bytes = parse_human_readable_size(args.min_size)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    main(min_size_bytes)

