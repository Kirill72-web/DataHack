import argparse
import sys
import os

from generator import generate_from_py


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run generator')
    parser.add_argument("--file", '-f', required=True)
    parser.add_argument("--row", '-r', required=False, default=10000)

    args = parser.parse_args()

    dfs = generate_from_py(args.file, int(args.row))

    for key in dfs.keys():
        dfs[key].to_csv(f"{args.file.lower()}_{key.lower()}.csv", index=False)
