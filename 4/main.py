from dataclasses import dataclass
import re


test_data = [
"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
"Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
"Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
"Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
"Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]

@dataclass
class Card:
    n: int
    winning: set[int]
    owned: set[int]

LINE_RE = re.compile(r"^Card +(\d+):(.+)\|(.+)$")

def parse_list_of_numbers(list_of_numbers: str) -> set[int]:
    split_list = list_of_numbers.strip().split()
    ret = set()
    for chars in split_list:
        try:
            ret.add(int(chars))
        except ValueError:
            continue
    
    return ret


def parse_line(line: str) -> Card:
    re_match = LINE_RE.fullmatch(line)
    if re_match is None:
        raise Exception(f"{line}")
    
    game_id, winning, owned = re_match.groups()

    return Card(int(game_id), parse_list_of_numbers(winning), parse_list_of_numbers(owned))

def find_winners(card: Card) -> int:
    number_winning_cards = len(card.owned & card.winning)
    if number_winning_cards == 0:
        return 0
    return 1 << number_winning_cards - 1


#n = sum([find_winners(parse_line(line.strip())) for line in open("input")])
#print(n)

all_cards = [parse_line(line.strip()) for line in open("input")]


i = 0
cards: dict[int, list[Card]] = {}
while i < len(all_cards):
    current_card = all_cards[i]
    cards_in_dict = cards.setdefault(current_card.n, [])
    cards_in_dict.append(current_card)
    for k in range(len(cards_in_dict)):
        num_matches = len(current_card.owned & current_card.winning)
        for j in range(num_matches):
            cards.setdefault(current_card.n + j + 1, []).append(all_cards[current_card.n + j])
    i += 1

number_of_all_cards = 0

for card_list in cards.values():
    number_of_all_cards += len(card_list)

print(number_of_all_cards)

