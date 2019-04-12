from enum import Enum, auto
from translate import t


class ComboInfo:

    def __init__(self, combo_type, display_name, rate):
        self.combo_type = combo_type
        self.display_name = display_name
        self.rate = rate


class Combo(Enum):
    INITIAL = auto(),
    ROYAL_FLUSH = auto(),
    STRAIGHT_FLUSH = auto(),
    FOUR_OF_KIND = auto(),
    FULL_HOUSE = auto(),
    FLUSH = auto(),
    STRAIGHT = auto(),
    THREE_OF_KIND = auto(),
    TWO_PAIR = auto(),
    PAIR = auto()


class ComboList:

    def __init__(self):
        self.combos = {
            Combo.INITIAL: ComboInfo(Combo.INITIAL, "combo.initial", 0),
            Combo.ROYAL_FLUSH: ComboInfo(Combo.ROYAL_FLUSH, "combo.royal-flush", 250),
            Combo.STRAIGHT_FLUSH: ComboInfo(Combo.STRAIGHT_FLUSH, "combo.straight-flush", 50),
            Combo.FOUR_OF_KIND: ComboInfo(Combo.FOUR_OF_KIND, "combo.4-of-kind", 25),
            Combo.FULL_HOUSE: ComboInfo(Combo.FULL_HOUSE, "combo.full-house", 9),
            Combo.FLUSH: ComboInfo(Combo.FLUSH, "combo.flush", 5),
            Combo.STRAIGHT: ComboInfo(Combo.STRAIGHT, "combo.straight", 4),
            Combo.THREE_OF_KIND: ComboInfo(Combo.THREE_OF_KIND, "combo.3-of-kind", 3),
            Combo.TWO_PAIR: ComboInfo(Combo.TWO_PAIR, "combo.two-pair", 2),
            Combo.PAIR: ComboInfo(Combo.PAIR, "combo.pair", 1)
        }

    def set_initial_balance(self, value):
        self.combos[Combo.INITIAL].rate = value

    def matchAny(self, hand):
        for c in list(Combo):
            if self.__match(c, hand):
                return self.combos[c]
        return None

    def __match(self, combo, hand):
        if combo == Combo.ROYAL_FLUSH:
            return self.__match(Combo.STRAIGHT_FLUSH, hand) and list(filter(lambda x: x.rank == "ace", hand.cards))
        if combo == Combo.STRAIGHT_FLUSH:
            return self.__match(Combo.FLUSH, hand) and self.__match(Combo.STRAIGHT, hand)
        if combo == Combo.FOUR_OF_KIND:
            return len(list(filter(lambda x: x == 4, hand.group_by_rank().values()))) == 1
        if combo == Combo.FULL_HOUSE:
            return self.__match(Combo.THREE_OF_KIND, hand) and self.__match(Combo.TWO_PAIR, hand)
        if combo == Combo.FLUSH:
            return len(set(map(lambda x: x.suit, hand.cards))) == 1
        if combo == Combo.STRAIGHT:
            ones = False
            for v in hand.group_by_rank().values():
                if v == 1:
                    ones = True
                elif ones:
                    return None
            return combo
        if combo == Combo.THREE_OF_KIND:
            return len(list(filter(lambda x: x == 3, hand.group_by_rank().values()))) == 1
        if combo == Combo.TWO_PAIR:
            return len(list(filter(lambda x: x == 2, hand.group_by_rank().values()))) == 2
        if combo == Combo.PAIR:
            return 2 in [v for k, v in hand.group_by_rank().items() if k in ['jack', 'queen', 'king', 'ace']]
        return None
