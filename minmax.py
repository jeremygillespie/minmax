from collections import namedtuple
import nashpy as nash
import numpy as np


class state:
    def __init__(self, prev=None, m_max=0, m_min=0, m_chance=0):
        self.moves_max = 1
        self.moves_min = 1
        self.moves_chance = 1
        self.game_over = False
        self._updated = False
        self._value = 0
        self._game = nash.Game(np.array([[1]], dtype=float))

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
        payoffs = np.empty((self.moves_max, self.moves_min), dtype=float)
        for m_max in range(self.moves_max):
            for m_min in range(self.moves_min):
                payoffs[m_max, m_min] = self._avg_outcome(m_max, m_min)
        self._game = nash.Game(payoffs)
        self._value = self._game[next(self.strategies)][0]

    def _avg_outcome(self, m_max, m_min):
        result = 0
        for m_chance in range(self.moves_chance):
            successor = self.__class__(self, m_max, m_min, m_chance)
            result += successor.value
        return result / self.moves_chance


class state_nonuniform(state):
    def __init__(self, prev=None, m_max=0, m_min=0, m_chance=0):
        state.__init__(self)
        self.chance_dist = np.array([1], dtype=float)

    def _avg_outcome(self, m_max, m_min):
        result = 0
        for m_chance, prob in enumerate(self.chance_dist):
            successor = self.__class__(self, m_max, m_min, m_chance)
            result += successor.value * prob
        return result / np.sum(self.chance_dist)


class rps(state):
    rock = 0
    paper = 1
    scissors = 2

    def __init__(self, prev=None, m_max=0, m_min=0, m_chance=0):
        state.__init__(self)

        if prev == None:
            self.moves_max = 3
            self.moves_min = 3
        else:
            self.moves_min = 1
            self.moves_max = 1
            self.game_over = True

            if m_max == m_min + 1 or m_max == m_min - 2:
                self.value = 1
            elif m_max == m_min - 1 or m_max == m_min + 2:
                self.value = -1
            else:
                self.value = 0


if __name__ == '__main__':
    r1 = rps()
    print(r1.value)
    for s in r1.strategies:
        print(s)

    r2 = rps(r1, 0, 0)
    print(r2.value)
    for s in r2.strategies:
        print(s)
