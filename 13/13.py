import rich
import sys
from typing import Tuple, List, Set
from util.read_input import read_input

print = rich.print

Point = Tuple[int, int]


class DotGrid:
    def __init__(self) -> None:
        self.points: Set[Point] = set()
        self.folds: List[Point] = []

    def add_point(self, p: Point) -> None:
        self.points.add(p)

    def add_fold(self, f: Point) -> None:
        self.folds.append(f)

    def print(self) -> None:
        max_x, _ = max(self.points, key=lambda point: point[0])
        _, max_y = max(self.points, key=lambda point: point[1])
        for y in range(max_y + 1):
            print()
            for x in range(max_x + 1):
                if (x, y) in self.points:
                    print("[bold magenta]#[/bold magenta] ", end="")
                else:
                    print(". ", end="")
        print()


def point_from_fold_def(direction_letter: str, val: str) -> Point:
    return (0, int(val)) if direction_letter == "y" else (int(val), 0)


def read_dots_input(f: str) -> DotGrid:
    dg = DotGrid()
    for line in read_input(f):
        if not line:
            continue
        elif line.startswith("fold along"):
            dg.add_fold(point_from_fold_def(*line.split(" ")[2].split("=")))
        else:
            x, y = [int(x) for x in line.split(",")]
            dg.add_point((x, y))
    return dg


def calculate_new_point(point: Point, fold: Point) -> Point:

    # Y-Fold
    if fold[0] == 0:
        fold_y = fold[1]
        x, y = point
        if y < fold_y:
            return point
        else:  # We're guaranteed that y != fold_y, so y > fold_y
            return (x, fold_y - (y - fold_y))
    # X-Fold
    else:
        fold_x = fold[0]
        x, y = point
        if x < fold_x:
            return point
        else:
            return (fold_x - (x - fold_x), y)


def make_fold(dg: DotGrid) -> DotGrid:
    new_dg = DotGrid()
    fold, new_dg.folds = dg.folds[0], dg.folds[1:]
    new_dg.points = {calculate_new_point(point, fold) for point in dg.points}
    return new_dg


def make_all_folds(dg: DotGrid) -> DotGrid:
    current_dg = dg
    while current_dg.folds:
        current_dg = make_fold(current_dg)
    current_dg.print()
    return current_dg


if __name__ == "__main__":
    f = sys.argv[1]
    print(len(make_fold(read_dots_input(f)).points))
    print(len(make_all_folds(read_dots_input(f)).points))
