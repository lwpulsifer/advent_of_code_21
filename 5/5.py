from collections import defaultdict
from util.read_input import read_input
from typing import DefaultDict, Iterable, List, Tuple
import sys

Point = Tuple[int, int]


class Vent:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Vent({self.start}, {self.end})"


def point_from_string(pointstring: str) -> Point:
    startnum, endnum = [int(num) for num in pointstring.split(",")]
    return (startnum, endnum)


def read_vent_input(f: str):
    vents: List[Vent] = []
    for line in read_input(f):
        start, end = line.split(" -> ")
        vents.append(Vent(point_from_string(start), point_from_string(end)))
    return vents


def move_towards(p1: Point, p2: Point) -> Point:
    if p1 == p2:
        return p1
    p1x, p1y = p1
    p2x, p2y = p2

    if p1x < p2x:
        newx = p1x + 1
    elif p1x > p2x:
        newx = p1x - 1
    else:
        newx = p1x

    if p1y < p2y:
        newy = p1y + 1
    elif p1y > p2y:
        newy = p1y - 1
    else:
        newy = p1y

    return (newx, newy)


def points_in_vent(vent: Vent, consider_diagonals: bool = False) -> Iterable[Point]:
    start_x, start_y = vent.start
    end_x, end_y = vent.end
    if not consider_diagonals and start_x != end_x and start_y != end_y:
        return ()

    point = vent.start
    while True:
        yield point
        if point == vent.end:
            return
        point = move_towards(point, vent.end)


def calculate_overlaps(vents: List[Vent], consider_diagonals: bool = False) -> int:
    points_covered: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    for vent in vents:
        for point in points_in_vent(vent, consider_diagonals):
            points_covered[point] += 1
    return len([val for _, val in points_covered.items() if val > 1])


if __name__ == "__main__":
    f = sys.argv[1]
    print(calculate_overlaps(read_vent_input(f)))
    print(calculate_overlaps(read_vent_input(f), True))
