from minmax import state


class deuces(state):
    def __init__(self):
        state.__init__(self)

    def successor(self, max_m, min_m, chance_m):
        return deuces()
