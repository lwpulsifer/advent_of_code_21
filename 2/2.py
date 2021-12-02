import sys
from util.read_input import read_input


def read_submarine_input(f):
    return [
        (command_type, int(inc))
        for (command_type, inc) in [line.split(" ") for line in read_input(f)]
    ]


basic_position_increments = {
    "forward": lambda pos, x: (pos[0] + x, pos[1]),
    "up": lambda pos, x: (pos[0], pos[1] - x),
    "down": lambda pos, x: (pos[0], pos[1] + x),
}


def calculate_basic_position(f):
    pos = (0, 0)
    for command_type, inc in read_submarine_input(f):
        pos = basic_position_increments[command_type](pos, inc)
    x, y = pos
    return x * y


complex_position_increments = {
    "forward": lambda pos, aim, x: ((pos[0] + x, pos[1] + aim * x), aim),
    "up": lambda pos, aim, x: (pos, aim - x),
    "down": lambda pos, aim, x: (pos, aim + x),
}


def calculate_complex_position(f):
    pos = (0, 0)
    aim = 0
    for command_type, inc in read_submarine_input(f):
        pos, aim = complex_position_increments[command_type](pos, aim, inc)
    x, y = pos
    return x * y


if __name__ == "__main__":
    f = sys.argv[1]
    print("Calculating sumbarine position for input file:", f)
    print("Simple:", calculate_basic_position(f))
    print("Complex:", calculate_complex_position(f))
