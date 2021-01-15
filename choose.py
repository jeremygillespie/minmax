import numpy as np
from math import comb


def choose(n, k, i):
    result = np.full((n), True, dtype=bool)
    needed = k
    checked = 0
    for j, val in np.ndenumerate(result):
        if needed == 0:
            result[j] = False
        elif val:
            remaining = n - checked - 1
            possible_false = comb(remaining, needed)

            if i >= possible_false:
                needed -= 1
                i -= possible_false
            else:
                result[j] = False

            checked += 1
    return result


def choose_all(n, k):
    # return a generator of all choices
    pass


def choose_array(arr, k, i):
    n = np.count_nonzero(arr)
    needed = k
    checked = 0
    for j, val in np.ndenumerate(arr):
        if needed == 0:
            arr[j] = False
        elif val:
            remaining = n - checked - 1
            possible_false = comb(remaining, needed)

            if i >= possible_false:
                needed -= 1
                i -= possible_false
            else:
                arr[j] = False

            checked += 1


if __name__ == '__main__':
    k = 3
    n = 6

    a = np.array(
        [[True, True, True], [False, False, False], [True, True, True]])

    for i in range(comb(n, k)):
        arr = np.copy(a)
        choose_array(arr, k, i)
        print(arr)
        print()
