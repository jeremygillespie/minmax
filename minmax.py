from collections import namedtuple
import nashpy as nash
import numpy as np

rock = 0
paper = 1
scissors = 2


class state:
    def __init__(self):
        self.max_moves = 1
        self.min_moves = 1
        self.chance_dist = [1.0]
        self.game_over = False

    def successor(self, max_m=0, min_m=0, chance_m=0):
        result = state()
        result.max_moves = 3
        result.min_moves = 3

        if max_m == min_m + 1 or max_m == min_m - 2:
            result.value = 1
        elif max_m == min_m - 1 or max_m == min_m + 2:
            result.value = -1
        else:
            result.value = 0

        result.game_over = True
        return result

    def calc_value(self):
        if not self.game_over:
            self.calc_strategy()

    def calc_strategy(self):
        payoffs = np.empty((self.max_moves, self.min_moves), dtype=float)

        for max_m in range(self.max_moves):
            for min_m in range(self.min_moves):
                payoffs[min_m, max_m] = self.avg_outcome(max_m, min_m)

        game = nash.Game(payoffs)
        self.strategy = next(game.support_enumeration())
        self.value = game[self.strategy][0]

    def avg_outcome(self, max_m, min_m):
        result = 0
        for chance_m, prob in enumerate(self.chance_dist):
            successor = self.successor(max_m, min_m, chance_m)
            successor.calc_value()
            result += successor.value * prob
        return successor.value


s = state()
s.calc_value()
print(s.value)

s = s.successor(rock, scissors)
s.calc_value()
print(s.value)

s = state()
s.calc_strategy()
print(s.strategy)
