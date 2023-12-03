from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
import string

test_data = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

ALL_SYMBOLS = string.punctuation.replace(".", "")
@dataclass
class Cord:
    x: int
    y: int

    def __add__(self, other: Cord) -> Cord:
        return Cord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Cord) -> Cord:
        return Cord(self.x - other.x, self.y + other.y)

    def __eq__(self, other: Cord) -> bool:
        return self.x == other.x and self.y == other.y

ADJACENT_MAP = [Cord(-1, -1), Cord(0, -1), Cord(1, -1), Cord(1, 0), Cord(1, 1), Cord(0, 1), Cord(-1, 1), Cord(-1, 0)]

@dataclass
class NumberSequence:
    number: int
    start: Cord
    length: int


def find_symbol_in_line(line: str, y: int) -> list[Cord]:
    ret = []
    for x, char in enumerate(line):
        if char in ALL_SYMBOLS:
            ret.append(Cord(x, y))
    return ret

def parse_known_number(known_number: str, x, y) -> NumberSequence:
    number_start = x - len(known_number)
    number_cord = Cord(number_start, y)
    return NumberSequence(int(known_number), number_cord, len(known_number))

def find_number_sequence_in_line(line: str, y: int) -> list[NumberSequence]:
    ret = []
    known_number = ""
    for x, char in enumerate(line):
        if char.isdigit():
            known_number += char
        elif len(known_number) != 0:
            ret.append(parse_known_number(known_number, x, y))
            known_number = ""
    try:
        ret.append(parse_known_number(known_number, len(line), y))
    except ValueError:
        pass

    return ret

def find_all_symbols(input_data: Iterable[str]) -> list[Cord]:
    all_symbol_cord = []
    for y, line in enumerate(input_data):
        all_symbol_cord.extend(find_symbol_in_line(line, y))
    
    return all_symbol_cord

def find_all_number_sequences(input_data: Iterable[str]) -> list[NumberSequence]:
    ret = []
    for y, line in enumerate(input_data):
        ret.extend(find_number_sequence_in_line(line, y))
    
    return ret



def is_number_adjacent_to_symbol(number: NumberSequence, symbols: list[Cord]) -> bool:
    for symbol in symbols:
        for adjacent in ADJACENT_MAP:
            new_cord = symbol + adjacent
            for i in range(number.length):
                new_number_cord = Cord(number.start.x + i, number.start.y)
                if new_number_cord == new_cord:
                    return True
    
    return False


input_data = open("input").readlines()
all_symbols = find_all_symbols(input_data)
all_numbers = find_all_number_sequences(input_data)

#all_symbols = find_all_symbols(test_data)
#all_numbers = find_all_number_sequences(test_data)
#print(is_number_adjacent_to_symbol(NumberSequence(467, Cord(0,0), 3), [Cord(3, 1)]))

n = 0
for number in all_numbers:
    if is_number_adjacent_to_symbol(number, all_symbols):
        n += number.number

print(n)
