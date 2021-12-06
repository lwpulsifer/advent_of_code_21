from typing import Counter, List
from util.read_input import read_input
import sys

# Number of days until a newly born fish can in turn create a new fish.
NEW_FISH_AGE: int = 8
# Number of days until a fish who has just created a new fish can do so again.
RESET_FISH_AGE: int = 6


def read_lanternfish_input(f: str) -> List[int]:
    return [int(x) for x in read_input(f)[0].split(",")]


def simulate_lanternfish(fish: List[int], num_days: int) -> int:
    current_fish: Counter[int] = Counter(fish)
    for _ in range(num_days):
        new_fish: Counter[int] = Counter()
        for age in range(NEW_FISH_AGE + 1):
            if age == 0:
                # Birth of new fish
                new_fish[NEW_FISH_AGE] = current_fish[age]
                # Old fish resetting
                new_fish[RESET_FISH_AGE] = current_fish[age]
            else:
                # Use += so that we don't overwrite the fish that have reset
                new_fish[age - 1] += current_fish[age]
        current_fish = new_fish

    return sum(current_fish.values())


if __name__ == "__main__":
    test_cases = {
        ("6_test.txt", 18): 26,
        ("6_test.txt", 80): 5934,
        ("6.txt", 80): 363101,
        ("6.txt", 256): 1644286074024,
    }
    for (f, num_days), expected_out in test_cases.items():
        lantern_fish = read_lanternfish_input(f)
        if (actual_out := simulate_lanternfish(lantern_fish, num_days)) != expected_out:
            print(f"Expected {expected_out}, got {actual_out}")
            sys.exit(1)
    else:
        print("Passed all test cases")
