# solutions.py
# Complete Solutions for Exercises 2.1 – 2.5 in Python
# Includes step-by-step explanations for 2.1 (Variable Elimination)
# and 2.2 (Blocked Clause Elimination)

# -----------------------------
# Exercise 2.1: Variable Elimination
# -----------------------------
def variable_elimination_step(formula, var):
    """
    Apply Variable Elimination (VE) on formula with given variable.
    formula: list of clauses (each clause is a list of literals)
    var: variable name (positive int)
    Returns simplified formula.
    """
    pos_clauses = [c for c in formula if var in c]
    neg_clauses = [c for c in formula if -var in c]
    rest_clauses = [c for c in formula if var not in c and -var not in c]

    print(f"\nEliminating variable x{abs(var)} from formula...")
    print(f"Positive clauses with x{var}: {pos_clauses}")
    print(f"Negative clauses with ¬x{var}: {neg_clauses}")
    print(f"Remaining clauses: {rest_clauses}")

    # Resolve each positive with each negative
    resolvents = []
    for p in pos_clauses:
        for n in neg_clauses:
            new_clause = sorted(list(set([lit for lit in p if lit != var] +
                                         [lit for lit in n if lit != -var])))
            if not any(-lit in new_clause for lit in new_clause):  # remove tautologies
                resolvents.append(new_clause)

    print(f"Generated resolvents: {resolvents}")

    # New formula is rest + resolvents (duplicates removed)
    new_formula = []
    for clause in rest_clauses + resolvents:
        if clause not in new_formula:
            new_formula.append(clause)

    print(f"Simplified formula after eliminating x{abs(var)}: {new_formula}")
    return new_formula

def exercise_2_1():
    # Represent formula: (x1 ∨ x2) ∧ (x1 ∨ ¬x4) ∧ (¬x1 ∨ x4 ∨ ¬x5)
    # ∧ (¬x1 ∨ ¬x3) ∧ (x2 ∨ ¬x3 ∨ x4) ∧ (¬x1 ∨ x3 ∨ ¬x2)
    F = [
        [1, 2],
        [1, -4],
        [-1, 4, -5],
        [-1, -3],
        [2, -3, 4],
        [-1, 3, -2]
    ]
    print("\n=== Exercise 2.1 ===")
    print("Original formula:", F)

    F_x1 = variable_elimination_step(F, 1)
    F_x1_x2 = variable_elimination_step(F_x1, 2)
    F_x2 = variable_elimination_step(F, 2)
    F_x2_x1 = variable_elimination_step(F_x2, 1)
    F_x5 = variable_elimination_step(F, 5)


# -----------------------------
# Exercise 2.2: Blocked Clause Elimination
# -----------------------------
def is_blocked_clause(clause, formula):
    """
    Check if a clause is blocked.
    Clause is blocked if there is a literal l in it such that all resolvents with ¬l are tautologies.
    """
    for lit in clause:
        tautology = True
        for other in [c for c in formula if -lit in c]:
            resolvent = list(set([l for l in clause if l != lit] + [l for l in other if l != -lit]))
            if not any(-l in resolvent for l in resolvent):
                tautology = False
                break
        if tautology:
            return True, lit
    return False, None

def exercise_2_2():
    # Formula: C1=(x1 ∨ ¬x2 ∨ ¬x3), C2=(¬x1 ∨ x2 ∨ x4),
    # C3=(¬x2 ∨ x3), C4=(x2 ∨ ¬x4), C5=(x1 ∨ x4)
    F = [
        [1, -2, -3],
        [-1, 2, 4],
        [-2, 3],
        [2, -4],
        [1, 4]
    ]
    print("\n=== Exercise 2.2 ===")
    step = 1
    changed = True
    while changed:
        changed = False
        for clause in F[:]:
            blocked, lit = is_blocked_clause(clause, F)
            if blocked:
                print(f"Step {step}: Clause {clause} is blocked on literal {lit} — removing it.")
                F.remove(clause)
                step += 1
                changed = True
                break
    print(f"Final formula after BCE: {F}")


# -----------------------------
# Exercise 2.3: QBF
# -----------------------------
def exercise_2_3():
    print("\n=== Exercise 2.3 ===")
    print("QParity2 ≡ ∃x1∃x2∀y.(y ⊕ (x1 ⊕ x2))")
    print("Truth: TRUE (since for any y, we can choose x1, x2 such that y = x1 ⊕ x2)")
    print("Prenex CNF form:")
    print("∃x1∃x2∀y.( (¬y ∨ ¬x1 ∨ ¬x2) ∧ (¬y ∨ x1 ∨ x2) ∧ (y ∨ ¬x1 ∨ x2) ∧ (y ∨ x1 ∨ ¬x2) )")


# -----------------------------
# Exercise 2.4: Weighted MaxSAT
# -----------------------------
def exercise_2_4():
    print("\n=== Exercise 2.4 ===")
    print("Original partial weighted MaxSAT formula:")
    print("(¬x1 ∨ x2 ∨ x3) ∧ (¬x1 ∨ ¬x2) ∧ (¬x3) ∧ (x1 ∨ ¬x2)^4 ∧ (x1 ∨ x2)^2 ∧ (x3)^1")
    print("\n(a) Blocking Variable Transformation applied:")
    print("Introduce b1, b2, ... for each soft clause, making them hard when ORed with bi.")
    print("\n(b) Optimal solution: x1=True, x2=False, x3=False; Cost = 1")
    print("\n(c) Example unsatisfiable cores: {¬x3, x3}, {¬x1∨¬x2, x1∨x2}")
    print("Minimum cost hitting set: {x3} with cost 1")


# -----------------------------
# Exercise 2.5: N-Queens SAT Solver
# -----------------------------
from pysat.solvers import Minisat22
from pysat.formula import CNF

def nqueens_sat_count(N):
    # SAT encoding: each row has exactly one queen; no attacks
    cnf = CNF()
    # Row constraints
    for i in range(N):
        cnf.append([i*N + j + 1 for j in range(N)])  # at least one in row
        for j1 in range(N):
            for j2 in range(j1+1, N):
                cnf.append([-(i*N + j1 + 1), -(i*N + j2 + 1)])  # at most one in row
    # Column constraints
    for j in range(N):
        for i1 in range(N):
            for i2 in range(i1+1, N):
                cnf.append([-(i1*N + j + 1), -(i2*N + j + 1)])
    # Diagonal constraints
    for i in range(N):
        for j in range(N):
            for k in range(1, N):
                if i+k < N and j+k < N:
                    cnf.append([-(i*N + j + 1), -((i+k)*N + (j+k) + 1)])
                if i+k < N and j-k >= 0:
                    cnf.append([-(i*N + j + 1), -((i+k)*N + (j-k) + 1)])

    solver = Minisat22(bootstrap_with=cnf)
    count = 0
    while solver.solve():
        model = solver.get_model()
        solver.add_clause([-lit for lit in model if lit > 0])
        count += 1
    solver.delete()
    return count

def exercise_2_5():
    print("\n=== Exercise 2.5 ===")
    for N in [4, 5, 8]:
        print(f"N={N} → {nqueens_sat_count(N)} solutions")


# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    exercise_2_1()
    exercise_2_2()
    exercise_2_3()
    exercise_2_4()
    exercise_2_5()
