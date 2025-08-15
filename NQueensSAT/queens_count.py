#!/usr/bin/env python3
"""
Count N-Queens solutions using a SAT solver (PySAT).
Usage: python queens_count.py 8
"""

import sys
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Glucose4  # switch to Minisat22 if needed

def var_id(r, c, N):
    return (r - 1) * N + c  # 1..N*N

def exactly_one(lits, cnf):
    cnf.append(lits[:])  # at least one
    for a, b in combinations(lits, 2):  # at most one (pairwise)
        cnf.append([-a, -b])

def build_nqueens_cnf(N):
    cnf = CNF()

    # Exactly one queen per row
    for r in range(1, N + 1):
        row = [var_id(r, c, N) for c in range(1, N + 1)]
        exactly_one(row, cnf)

    # At most one queen per column
    for c in range(1, N + 1):
        col = [var_id(r, c, N) for r in range(1, N + 1)]
        for a, b in combinations(col, 2):
            cnf.append([-a, -b])

    # At most one per main diag (r - c const)
    d = {}
    for r in range(1, N + 1):
        for c in range(1, N + 1):
            d.setdefault(r - c, []).append(var_id(r, c, N))
    for bucket in d.values():
        for a, b in combinations(bucket, 2):
            cnf.append([-a, -b])

    # At most one per anti-diag (r + c const)
    ad = {}
    for r in range(1, N + 1):
        for c in range(1, N + 1):
            ad.setdefault(r + c, []).append(var_id(r, c, N))
    for bucket in ad.values():
        for a, b in combinations(bucket, 2):
            cnf.append([-a, -b])

    return cnf

def count_solutions(N):
    cnf = build_nqueens_cnf(N)
    count = 0
    with Glucose4(bootstrap_with=cnf.clauses) as solver:
        while solver.solve():
            count += 1
            model = solver.get_model()
            assign = {abs(l): (l > 0) for l in model}
            # block this model (only our vars 1..N*N)
            block = [(-v if assign.get(v, False) else v) for v in range(1, N*N + 1)]
            solver.add_clause(block)
    return count

def main():
    if len(sys.argv) != 2:
        print("Usage: python queens_count.py N")
        sys.exit(1)
    N = int(sys.argv[1])
    if N <= 3:
        print("N must be > 3")
        sys.exit(1)
    print(count_solutions(N))

if __name__ == "__main__":
    main()
