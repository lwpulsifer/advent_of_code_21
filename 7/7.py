from util.read_input import read_input
from typing import Dict, List, Callable
import sys


def read_crab_input(f: str) -> List[int]:
    return [int(pos) for pos in read_input(f)[0].split(",")]


def sum_indices(n: int) -> int:
    """
    Gets the sum from 1..n inclusive using the closed-form expression.
    It should be ok to use integer division here because even * odd is always even.
    """
    return (n * (n + 1)) // 2


position_algorithms: Dict[str, Callable[[int, int], int]] = {
    "pure_position": lambda anchor, pos: abs(anchor - pos),
    "additive_position": lambda anchor, pos: sum_indices(abs(anchor - pos)),
}


def calculate_minimum_combined_offset(positions: List[int], position_algo: str) -> int:
    min_offset = float("inf")
    for i in range(max(positions)):
        min_offset = min(
            min_offset,
            sum((position_algorithms[position_algo](pos, i) for pos in positions)),
        )
    return int(min_offset)


if __name__ == "__main__":
    test_cases_1: Dict[str, int | None] = {
        "7_test.txt": 37,
        "7.txt": 341558,
    }
    test_cases_2: Dict[str, int | None] = {
        "7_test.txt": 168,
        "7.txt": 93214037,
    }
    test_cases = [test_cases_1, test_cases_2]
    test_algos = ["pure_position", "additive_position"]
    for test_case, test_algo in zip(test_cases, test_algos):
        for f, expected in test_case.items():
            actual = calculate_minimum_combined_offset(read_crab_input(f), test_algo)
            if actual != expected and expected is not None:
                print(f"Expected f{expected} for file {f}, got {actual}")
                sys.exit(1)
            else:
                print(f"Got {actual} for file {f}")
        else:
            print("Passed tests")
