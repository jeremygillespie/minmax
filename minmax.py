from collections import namedtuple
import nashpy as nash
import numpy as np


class state:
    def __init__(self):
        self.max_moves = 1
        self.min_moves = 1
        self.chance_dist = [1.0]
        self.game_over = True
        self._updated = False
        self._value = 0
        self._game = nash.Game(np.array([[1]], dtype=float))

    def successor(self, max_m=0, min_m=0, chance_m=0):
        return state()

    def _update(self):
        if not self.game_over and not self._updated:
            self._updated = True
            self._calc_strat()

    def _get_strats(self):
        self._update()
        return self._game.support_enumeration()

    strategies = property(_get_strats)

    def _get_value(self):
        self._update()
        return self._value

    def _set_value(self, val):
        self._value = val

    value = property(_get_value, _set_value)

    def _calc_strat(self):
        payoffs = np.empty((self.max_moves, self.min_moves), dtype=float)

        for max_m in range(self.max_moves):
            for min_m in range(self.min_moves):
                payoffs[max_m, min_m] = self._avg_outcome(max_m, min_m)

        self._game = nash.Game(payoffs)
        self._value = self._game[next(self.strategies)][0]

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


class test(state):
    def __init__(self):
        state.__init__(self)
        self.max_moves = 3
        self.game_over = False

    def successor(self, max_m=0, min_m=0, chance_m=0):
        result = test()
        result.value = 1.0
        result.game_over = True
        return result


r1 = test()
print(r1.value)
for s in r1.strategies:
    print(s)

r2 = r1.successor(0)
print(r2.value)
for s in r2.strategies:
    print(s)
