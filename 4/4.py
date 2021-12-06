from typing import List, Tuple
from util.read_input import read_input
import sys


class BoardEntry:
    def __init__(self, num: int):
        self.num = num
        self.marked = False

    def __repr__(self) -> str:
        return f"{self.num}"


class Board:
    def __init__(self, rows: List[List[int]]):
        self.rows = [[BoardEntry(num) for num in l] for l in rows]
        self.has_won = False

    def __repr__(self) -> str:
        return f"{self.rows}\n"

    def is_winner(self):
        for row in self.rows:
            if all([entry.marked for entry in row]):
                return True
        for i in range(len(self.rows[0])):
            if all([row[i].marked for row in self.rows]):
                return True
        return False

    def flat_rows(self) -> List[BoardEntry]:
        flat_rows: List[BoardEntry] = []
        for row in self.rows:
            flat_rows.extend(row)
        return flat_rows


def read_bingo_input(f: str) -> Tuple[List[int], List[Board]]:
    lines: List[str] = read_input(f)
    guesses: List[int] = [int(x) for x in lines[0].split(",")]
    boards: List[Board] = []
    current_board_rows: List[List[int]] = []
    for line in lines[2:]:
        if not line and current_board_rows:
            boards.append(Board(current_board_rows))
            current_board_rows = []
        elif not line:
            continue
        else:
            current_board_rows.append([int(x) for x in line.split()])
    boards.append(Board(current_board_rows))
    return (guesses, boards)


def calculate_bingo_score(board: Board, last_guess: int) -> int:
    unmarked_numbers = [entry.num for entry in board.flat_rows() if not entry.marked]
    return sum(unmarked_numbers) * last_guess


def calculate_bingo_scores(guesses: List[int], boards: List[Board]) -> int:
    for guess in guesses:
        for board in boards:
            for row in board.rows:
                for entry in row:
                    if entry.num == guess:
                        entry.marked = True
            if board.is_winner():
                return calculate_bingo_score(board, guess)
    return -1


def calculate_last_bingo_scores(guesses: List[int], boards: List[Board]) -> int:
    num_remaining = len(boards)
    for guess in guesses:
        for board in boards:
            if board.has_won:
                continue
            for row in board.rows:
                for entry in row:
                    if entry.num == guess:
                        entry.marked = True
            if board.is_winner():
                if num_remaining == 1:
                    return calculate_bingo_score(board, guess)
                board.has_won = True
                num_remaining -= 1
    return -1


if __name__ == "__main__":
    f = sys.argv[1]
    print(calculate_bingo_scores(*read_bingo_input(f)))
    print(calculate_last_bingo_scores(*read_bingo_input(f)))
