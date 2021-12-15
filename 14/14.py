import rich

print = rich.print

import sys
from typing import Counter, Dict, List
from util.read_input import read_input


def read_polymer_input(f: str):
    lines = [line for line in read_input(f) if line]
    initial_polymer = lines[0]
    pairs = {key: val for key, val in [line.split(" -> ") for line in lines[1:]]}
    return initial_polymer, pairs


def pairs(s: str) -> List[str]:
    return [s[i : i + 2] for i in range(len(s) - 1)]


def calculate_polymers(
    initial_polymer: str, replacement_pairs: Dict[str, str], num_steps: int = 10
) -> int:
    current_polymer = Counter(pairs(initial_polymer))
    total_chars = Counter(initial_polymer)
    for i in range(num_steps):
        new_polymer: Counter[str] = current_polymer.copy()
        for pair, count in current_polymer.items():
            replacement_char = replacement_pairs[pair]
            total_chars[replacement_char] += count
            new_polymer[pair] -= count
            char1, char2 = pair
            new_polymer[char1 + replacement_char] += count
            new_polymer[replacement_char + char2] += count
        current_polymer = new_polymer
        print("Steps completed", i + 1)
        print("Total chars:", sum(total_chars.values()))
    return max(total_chars.values()) - min(total_chars.values())


if __name__ == "__main__":
    f = sys.argv[1]
    print(calculate_polymers(*read_polymer_input(f), 40))
