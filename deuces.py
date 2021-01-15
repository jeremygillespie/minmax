from minmax import state
import numpy as np
from choose import choose
from math import comb

suits = ["d", "c", "h", "s"]
vals = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def suit(card):
    return card % 4


def val(card):
    return int(card/4)


def card_str(card):
    return vals[val(card)] + suits[suit(card)]


player_max = True
player_min = False


class deuces(state):
    def __init__(self, prev=None, m_max=0, m_min=0, m_chance=0, cards=16):
        state.__init__(self)

        if prev == None:
            self.cards = cards
            self.moves_chance = comb(self.cards, int(self.cards/2))

        elif prev.moves_chance > 1:
            self.cards = prev.cards

            deck = np.arange(self.cards, dtype=int)
            mask_max = choose(self.cards, int(self.cards/2), m_chance)
            mask_min = np.logical_not(mask_max)
            self.hand_max = deck[mask_max]
            self.hand_min = deck[mask_min]

            if mask_max[0]:
                self._calc_possible(player_max)
            else:
                self._calc_possible(player_min)

            self.to_beat = np.array([], dtype=int)

        else:
            pass
            # update game state
            # check if game over
            # set up next move

    def _calc_possible(self, turn):
        if turn == player_max:
            hand = self.hand_max
        else:
            hand = self.hand_min

        self.possible = []

        if self.to_beat.size == 0:
            # all possible plays with only one value
            pass

        else:
            # all possible plays with:
            # size == to_beat.size and
            # only one value and
            # ( val > to_beat.val or
            # val == to_beat.val and play.high_card > to_beat.high_card )
            pass

        if turn == player_max:
            self.turn = player_max
            self.moves_max = len(self.possible)
        else:
            self.turn = player_min
            self.moves_min = len(self.possible)

    def __str__(self):
        result = ""

        result += "Max player's hand: "
        for card in self.hand_max:
            result += card_str(card) + ", "
        result += "\n"

        result += "Min player's hand: "
        for card in self.hand_min:
            result += card_str(card) + ", "
        result += "\n"

        result += "Cards to beat: "
        for card in self.to_beat:
            result += card_str(card) + ", "
        result += "\n"

        if self.turn == player_max:
            result += "Max to play"
        else:
            result += "Min to play"

        return result


d = deuces(cards=20)
d = deuces(d, m_chance=184755)
print(d)
