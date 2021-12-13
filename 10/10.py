from util.read_input import read_input
from typing import Dict, List, Tuple
from collections import deque
import sys

PAIRS: Dict[str, str] = {
    "{": "}",
    "[": "]",
    "<": ">",
    "(": ")",
}

BAD_BRACKET_VALUES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

AUTOCOMPLETE_SCORING_VALUES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def score_incomplete_line(current_brackets: deque[str]) -> int:
    score = 0
    while current_brackets:
        score *= 5
        bracket = current_brackets.pop()
        score += AUTOCOMPLETE_SCORING_VALUES[PAIRS[bracket]]
    return score


def get_middle_score(items: List[int]) -> int:
    return sorted(items)[len(items) // 2]


def find_bracket_errors(lines: List[str]) -> Tuple[int, int]:
    bad_brackets: List[str] = []
    incomplete_line_scores: List[int] = []
    for line in lines:
        current_pairs: deque[str] = deque()
        for char in line:
            if current_pairs and PAIRS[current_pairs[-1]] == char:
                current_pairs.pop()
            elif char in PAIRS.values():
                bad_brackets.append(char)
                break
            else:
                current_pairs.append(char)
        else:
            incomplete_line_scores.append(score_incomplete_line(current_pairs))

    return (
        sum([BAD_BRACKET_VALUES[bad_bracket] for bad_bracket in bad_brackets]),
        get_middle_score(incomplete_line_scores),
    )


if __name__ == "__main__":
    f = sys.argv[1]
    print(find_bracket_errors(read_input(f)))
