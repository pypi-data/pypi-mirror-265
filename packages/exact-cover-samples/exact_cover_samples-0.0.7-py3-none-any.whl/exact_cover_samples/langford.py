import numpy as np

def langford(n):
    """
    generate the exact cover problem for the Langford problem of size n

    e.g. for n=3:
    this would map to the following abbreviated cover problem
        1s1s3 exactyl one space between slots 1 and 3
        1s2s4
        1s3s5
        1s4s6
        2s1s4 exactly 2 spaces between slots 1 and 4
        2s2s5
        2s3s6
        3s1s5 you get the gist
        3s2s6
    which once turned into a boolean array gives
        [ True, False, False,  True, False,  True, False, False, False],
        [ True, False, False, False,  True, False,  True, False, False],
        [ True, False, False, False, False,  True, False,  True, False],
        [ True, False, False, False, False, False,  True, False,  True],
        [False,  True, False,  True, False, False,  True, False, False],
        [False,  True, False, False,  True, False, False,  True, False],
        [False,  True, False, False, False,  True, False, False,  True],
        [False, False,  True,  True, False, False, False,  True, False],
        [False, False,  True, False,  True, False, False, False,  True],
    """
    # the number of columns is 3*n
    L = []
    columns = 3*n
    for i in range(1, n+1):
        for j in range(1, 2*n):
            k = i + j + 1
            if k > 2*n:
                break
            line = np.zeros(columns, dtype=bool)
            line[i-1] = True
            line[n+j-1] = True
            line[n+k-1] = True
            L.append(line)
    return np.array(L)

def pretty(problem_data, solution):
    """
    pretty print a solution to the Langford problem
    pass the problem data (as output by the above)
    and the solution found by the exact cover solver
    returns an array of numbers in the 1..n range


    """
    n = problem_data.shape[1] // 3
    # print(f"{n=}")
    if isinstance(solution[0], (list, np.ndarray)):
        raise ValueError("expecting a 1D solution")
    s = np.zeros(2*n, dtype=int)
    for i in solution:
        pb_line = problem_data[i]
        j = np.argwhere(pb_line[:n])[0][0]
        w = np.argwhere(pb_line[n:]).ravel()
        for k in w:
            s[k] = j+1
    return s

from exact_cover_py import exact_covers
import pandas as pd

def mass_solve(r, long=False):
    for n in r:
        p = langford(n)
        pd.DataFrame(p).to_csv(f"langford-{n}.csv", header=False, index=False)
        s = list(exact_covers(p))
        pd.DataFrame(s).to_csv(f"langford-{n}-solutions.csv", header=False, index=False)
        print(f"{n=} has {len(s)} solutions")
        if not long:
            continue
        if not s:
            print(f"{n} has no solution")
        else:
            for i, sol in enumerate(s, 1):
                print(f"{n=} {i}-th sol = {pretty(p, sol)}")

def all():
    mass_solve((3, 4, 5, 6, 7, 8, 9, 10, 11), long=False)
