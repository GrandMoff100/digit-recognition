import sys

from .generate import Dataset

if __name__ == "__main__":
    Dataset(*map(int, sys.argv[1:])).generate_all()  # type: ignore
