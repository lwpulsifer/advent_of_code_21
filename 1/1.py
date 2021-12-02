import sys
from typing import List
from util.read_input import read_input


def read_input_int(f: str) -> List[int]:
    return [int(l) for l in read_input(f)]


def track_increasing_depth(f: str) -> int:
    count = 0
    for i in range(1, len(depths := read_input_int(f))):
        if depths[i] > depths[i - 1]:
            count += 1
    return count


def track_increasing_depth_sliding_window(f: str, window_size: int = 3) -> int:
    count = 0
    for i in range(1, len(depths := read_input_int(f)) - window_size + 1):
        if sum(depths[i : i + window_size]) > sum(depths[i - 1 : i - 1 + window_size]):
            count += 1
    return count


if __name__ == "__main__":
    f = sys.argv[1]
    print("Increasing depth count:", track_increasing_depth(f))
    print("Sliding window count:", track_increasing_depth_sliding_window(f))
