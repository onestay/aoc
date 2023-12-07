from __future__ import annotations

from enum import Enum, auto
from functools import total_ordering
from pathlib import Path

cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

@total_ordering
class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()
    
    def __gt__(self, other):
        if not isinstance(other, HandType):
            return NotImplemented
        return self.value > other.value

    def __hash__(self) -> int:
        return super().__hash__()

input_file = (Path(__file__).parent / "input.test").open()
input_data = [line.strip() for line in input_file.readlines()]

games: dict[str, int] = {}
for line in input_data:
    hand, bet = line.split(" ")
    games[hand] = int(bet)

def create_char_occurrence_dict(s: str) -> dict[str, int]:
    ret: dict[str, int] = {}
    for char in s:
        ret[char] = ret.get(char, 0) + 1
    if 'J' in ret:
        max_pair = max(ret.items(), key=lambda x: x[1])
        if max_pair[0] == "J":
            return ret
        else:
            ret[max_pair[0]] = max_pair[1] + ret["J"]
    return ret


def find_hand_type(hand: str) -> HandType:
    if all(hand[0] == char for char in hand):
        return HandType.FIVE_OF_A_KIND
    
    char_occ_dict = create_char_occurrence_dict(hand)
    four_kind_have_4 = False
    four_kind_have_1 = False
    full_house_have_3 = False
    full_house_have_2 = False
    if len(char_occ_dict) == 2:
        for v in char_occ_dict.values():
            if v == 4:
                four_kind_have_4 = True
            if v == 1:
                four_kind_have_1 = True
            if v == 2:
                full_house_have_2 = True
            if v == 3:
                full_house_have_3 = True
    
        if four_kind_have_4 and four_kind_have_1:
            return HandType.FOUR_OF_A_KIND
        
        if full_house_have_2 and full_house_have_3:
            return HandType.FULL_HOUSE
    
    if len(char_occ_dict) == 3:
        three_kind_have_3 = False
        three_kind_have_1_1 = False
        three_kind_have_1_2 = False

        two_pair_have_2_1 = False
        two_pair_have_2_2 = False
        two_pair_have_1 = False
        for v in char_occ_dict.values():
            if v == 3:
                three_kind_have_3 = True
            if v == 1 and not three_kind_have_1_1:
                three_kind_have_1_1 = True
            elif v == 1:
                three_kind_have_1_2 = True
            
            if v == 1:
                two_pair_have_1 = True
            
            if v == 2 and not two_pair_have_2_1:
                two_pair_have_2_1 = True
            elif v == 2:
                two_pair_have_2_2 = True
        
        if three_kind_have_3 and three_kind_have_1_1 and three_kind_have_1_2:
            return HandType.THREE_OF_A_KIND
        
        if two_pair_have_2_1 and two_pair_have_2_2 and two_pair_have_1:
            return HandType.TWO_PAIR
    if len(char_occ_dict) == 4:
        return HandType.ONE_PAIR
    
    return HandType.HIGH_CARD

type_map: dict[HandType, list[str]] = {}

for s in games:
    hand_type = find_hand_type(s)
    print(f"{s}: {hand_type}")
    type_map.setdefault(hand_type, []).append(s)

def key_func(s: str) -> list[int]:
    a = []
    for char in s:
        a.append(cards.index(char))
    return a

for k in type_map.values():
    if len(k) != 1:
        k.sort(key=key_func, reverse=True)
        print(k)

score = 0
rank = 1
for hand_type in HandType:
    if hand_type in type_map:
        hand = type_map[hand_type]
        for current_hand in hand:
            score += games[current_hand] * rank 
            rank += 1

print(score)