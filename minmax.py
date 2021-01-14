from collections import namedtuple
import nashpy as nash
import numpy as np


class state:
    def __init__(self):
        self.max_moves = 1
        self.min_moves = 1
        self.chance_dist = [1.0]
        self.game_over = True
        self.value = 0
        self.strategy = (np.array([1.0]), np.array([1.0]))

    def successor(self, max_m=0, min_m=0, chance_m=0):
        return state()

    def update(self):
        if not self.game_over:
            self._calc_strat()

    def _calc_strat(self):
        payoffs = np.empty((self.max_moves, self.min_moves), dtype=float)

        for max_m in range(self.max_moves):
            for min_m in range(self.min_moves):
                payoffs[min_m, max_m] = self._avg_outcome(max_m, min_m)

        game = nash.Game(payoffs)
        self.strategy = next(game.support_enumeration())
        self.value = game[self.strategy][0]

    def _avg_outcome(self, max_m, min_m):
        result = 0
        for chance_m, prob in enumerate(self.chance_dist):
            successor = self.successor(max_m, min_m, chance_m)
            result += successor.value * prob
        return successor.value


class rps(state):
    rock = 0
    paper = 1
    scissors = 2

    def __init__(self, game_over=False):
        if game_over:
            state.__init__(self)
        else:
            state.__init__(self)
            self.max_moves = 3
            self.min_moves = 3
            self.game_over = False

    def successor(self, max_m=0, min_m=0, chance_m=0):
        result = rps(game_over=True)

        if max_m == min_m + 1 or max_m == min_m - 2:
            result.value = 1
        elif max_m == min_m - 1 or max_m == min_m + 2:
            result.value = -1
        else:
            result.value = 0

        return result


r1 = rps()
r1.update()
print(r1.value)
print(r1.strategy)

r2 = r1.successor(rps.rock, rps.paper)
r2.update()
print(r2.value)
print(r2.strategy)
