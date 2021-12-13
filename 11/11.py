from util.read_input import read_input
from typing import List, Tuple
import sys

MAX_ENERGY = 9


def read_octo_input(f: str) -> List[List[int]]:
    return [[int(num) for num in line] for line in read_input(f)]


Position = Tuple[int, int]


def get_adjacent_points(
    position: Position, octopodes: List[List[int]]
) -> List[Position]:
    row_dex, col_dex = position
    adjacent_points: List[Position] = []

    adjacent_point_indices = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]

    for row_mod, col_mod in adjacent_point_indices:
        row = row_dex + row_mod
        col = col_dex + col_mod
        if row < 0 or row >= len(octopodes):
            continue
        elif col < 0 or col >= len(octopodes[0]):
            continue
        else:
            adjacent_points.append((row, col))
    return adjacent_points


def print_table(table: List[List[int]]):
    print("\n".join(["".join([str(octo) for octo in row]) for row in table]))


def simulate_octopodes(octopodes: List[List[int]], iterations: int = 100) -> int:
    current_octopodes: List[List[int]] = [row[:] for row in octopodes]
    total_flashes = 0
    for step in range(iterations):

        # Add one to all
        current_octopodes = [[octo + 1 for octo in row] for row in current_octopodes]

        appended = True
        to_flash: List[Position] = []
        has_flashed: List[Position] = []
        while appended:
            appended = False
            for row_dex, row in enumerate(current_octopodes):
                for col_dex, octo in enumerate(row):
                    if octo > MAX_ENERGY and (row_dex, col_dex) not in has_flashed:
                        to_flash.append((row_dex, col_dex))
                        appended = True
            while to_flash:
                flash_row, flash_col = to_flash.pop()
                for flashed_row, flashed_col in get_adjacent_points(
                    (flash_row, flash_col), current_octopodes
                ):
                    current_octopodes[flashed_row][flashed_col] += 1
                has_flashed.append((flash_row, flash_col))
                total_flashes += 1
        for row, col in has_flashed:
            current_octopodes[row][col] = 0
        print("Step:", step + 1)
        print_table(current_octopodes)
        if all([all([octo == 0 for octo in row]) for row in current_octopodes]):
            print(f"Synchronized at step {step + 1}")
        print()

    return total_flashes


if __name__ == "__main__":
    f = sys.argv[1]
    if len(sys.argv) > 2:
        print(simulate_octopodes(read_octo_input(f), int(sys.argv[2])))
    else:
        print(simulate_octopodes(read_octo_input(f)))
