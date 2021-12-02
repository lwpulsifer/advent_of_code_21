import os
from typing import List


def read_input(f: str) -> List[str]:
    with open(os.path.join(os.getcwd(), f), "r") as in_file:
        return [line.strip(" \n") for line in in_file.readlines()]
