from dataclasses import dataclass
from typing import Any, Generator, TypeAlias


data = [line.strip() for line in open("5/input").readlines()]

@dataclass
class Map:
    source: int
    dest: int
    range: int


ListOfMappings: TypeAlias = list[tuple[int, int]]


def parse_data(data: list[str]) -> tuple[list[list[Map]], list[int]]:
    maps: list[list[Map]] = []
    seeds = [int(n) for n in data[0].split(" ")[1:]]
    map_location = 2
    for i in range(7):
        d, ret = parse_map(data, map_location)
        maps.append(d)
        map_location = map_location + ret + 2
    return maps, seeds

def parse_map(data: list[str], start: int) -> tuple[list[Map], int]:
    i = 1
    ret = []
    while i+start < len(data):
        if len(data[start + i]) == 0:
            break

        dest_range, source_range, range_length = data[start + i].split()
        ret.append(Map(int(source_range), int(dest_range), int(range_length)))
        i += 1
    return ret, i - 1

def generate_range_map(dest_range: int, source_range: int, range_length: int, num_range: dict[int,int]):
    for i in range(range_length):
        num_range[source_range + i] = dest_range + i

def fill_range_map(num_range: dict[int, int]):
    i = 1
    while num_range.get(i) is None:
        num_range[i] = i
        i += 1

def inner(maps: list[Map], seed: int) -> int:
    for r in maps:
        if seed in range(r.source, r.source + r.range):
            seed += r.dest - r.source
            return seed
    return seed

def walk_map(maps: list[list[Map]], seed: int):
    for map in maps:
        seed = inner(map, seed)
    return seed

test_data = [
"soil-to-fertilizer map:",
"50 98 2",
"52 50 48",
]


map_list, seeds = parse_data(data)
print("parsed")

def all_seeds_generator(start, length):
        for s in range(start, start + length):
            yield s

seed_pairs = list(zip(seeds[::2], seeds[1::2]))
generator_functions = [all_seeds_generator(start, length) for start, length in seed_pairs]

def find(seed_pairs: tuple[int, int]) -> int:
    print(f"starting at {seed_pairs[0]} for {seed_pairs[1]}")
    lowest = None
    for seed in all_seeds_generator(seed_pairs[0], seed_pairs[1]):
        current_location = walk_map(map_list, seed)

        if lowest is None or current_location < lowest:
            lowest = current_location
    return lowest or 0
    
#for pair in seed_pairs:
#    print(find(pair))

def inner_rev(map: list[Map], seed: int) -> int:
    for r in map:
        if seed in range(r.dest, r.dest + r.range):
            seed -= r.dest - r.source
            return seed
    return seed

def is_valid_seed(seed_num: int, seed_pairs: list[tuple[int,int]]) -> bool:
    for seed_pair in seed_pairs:
        if seed_num in range(seed_pair[0], seed_pair[0] + seed_pair[1]):
            return True
    return False

def find_reversed():
    print("starting reverse search")
    i = 67832336
    while True:
        next_step = i
        for map in reversed(map_list):
            next_step = inner_rev(map, next_step)
        if is_valid_seed(next_step, seed_pairs):
            print(f"rev search result location {i} for seed {next_step}")
            return i
        i += 1

print(find_reversed())