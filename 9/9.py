from util.read_input import read_input
from typing import DefaultDict, List, Set, Tuple
import sys
from collections import deque
import math

MAX_HEIGHT = 9


Position = Tuple[int, int]
CaveMap = DefaultDict[Position, int]


def read_lava_tube_input(f: str) -> Tuple[CaveMap, int, int]:
    cave_map: CaveMap = DefaultDict(lambda: 10)
    input_lines = read_input(f)
    h = 0
    w = 0
    for row, heights in enumerate(input_lines):
        h = max(row, h)
        for col, height in enumerate(list(heights)):
            cave_map[(row, col)] = int(height)
            w = max(col, w)
    return cave_map, w + 1, h + 1


def get_adjacent_points(position: Position, cave_map: CaveMap) -> List[Position]:
    row_dex, col_dex = position
    adjacent_points: List[Position] = []

    adjacent_point_indices = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    ]

    for row_mod, col_mod in adjacent_point_indices:
        point_position = (row_dex + row_mod, col_dex + col_mod)
        adjacent_height = cave_map[point_position]
        if adjacent_height <= MAX_HEIGHT:
            adjacent_points.append((point_position))
    return adjacent_points


def is_low_point(position: Position, cave_map: CaveMap) -> bool:
    row_dex, col_dex = position
    height = cave_map[(row_dex, col_dex)]
    return all(
        [
            height < cave_map[position]
            for position in get_adjacent_points(position, cave_map)
        ]
    )


def find_low_points(cave_map: CaveMap, width: int, height: int) -> List[Position]:
    low_points: List[Position] = []
    for row_dex in range(height):
        for col_dex in range(width):
            current_pos = (row_dex, col_dex)
            height = cave_map[current_pos]
            if is_low_point(current_pos, cave_map):
                low_points.append(current_pos)
    return low_points


def calculate_risk_levels(cave_map: CaveMap, width: int, height: int) -> int:
    low_points = find_low_points(cave_map, width, height)
    return sum((cave_map[low_point] + 1 for low_point in low_points))


def calculate_basin_sizes(cave_map: CaveMap, width: int, height: int):
    low_points = find_low_points(cave_map, width, height)
    basin_sizes: List[int] = []

    for low_point in low_points:
        points_to_process: deque[Position] = deque([low_point])
        points_processed: Set[Position] = set()

        # BFS to get the full basin for each low point
        while points_to_process:
            curr_point = points_to_process.popleft()
            new_points = [
                point
                for point in get_adjacent_points(curr_point, cave_map)
                if cave_map[point] > cave_map[curr_point]
                and cave_map[point] != MAX_HEIGHT
                and point not in points_processed
            ]
            points_to_process.extend(new_points)
            points_processed.add(curr_point)

        basin_sizes.append(len(points_processed))

    return math.prod(sorted(basin_sizes, reverse=True)[:3])


if __name__ == "__main__":
    f = sys.argv[1]
    print(calculate_risk_levels(*read_lava_tube_input(f)))
    print(calculate_basin_sizes(*read_lava_tube_input(f)))
