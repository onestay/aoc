from __future__ import annotations
import re
from dataclasses import dataclass

parser_regex = re.compile(r"Game (\d+):(?: ?(?:(\d+) (?:blue|red|green),? ?){1,3}(?:;|$))+")

test_data = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}

@dataclass
class Game:
    gid: int
    pulls: list[dict[str, int]]

def parse_line(line: str) -> Game:
    game_tag, pulls = line.split(":")
    gid = int(game_tag.split(" ")[1])
    pulls = pulls.split(";")
    result_dict_list = []
    for pull in pulls:
        pull = pull.strip()
        n_colors = pull.split(",")
        result_dict = {}
        for n_color in n_colors:
            n_color = n_color.strip()
            n, color = n_color.split(" ")
            result_dict[color] = int(n)
        result_dict_list.append(result_dict)
    
    return Game(gid, result_dict_list)

def is_possible(game: Game) -> bool:
    for pull in game.pulls:
        for limit_color in limits:
            if limits[limit_color] < pull.get(limit_color, 0):
                return False

        
    return True

def min_cubes(game: Game) -> int:
    minc = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for pull in game.pulls:
        for limit in limits:
            if pull.get(limit, 0) > minc[limit]:
                minc[limit] = pull[limit]

    return minc["blue"] * minc["green"] * minc["red"]


n = 0

for data in open("input"):
    game = parse_line(data)
    #n += game.gid if is_possible(game) else 0
    n += min_cubes(game)


print(n)


