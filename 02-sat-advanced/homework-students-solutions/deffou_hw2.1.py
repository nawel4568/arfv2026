from pysmt.shortcuts import And, Or, Not, Iff, ExactlyOne, Solver, Symbol, BOOL

# list of numbers
numbers = list(range(1, 10))

assertions = []

def print_sudoku(model, vv):
    for i in numbers:
        if i % 3 == 1 and i != 1:
            print("-" * 21)  # horizontal separator
        row_values = []
        for j in numbers:
            if j % 3 == 1 and j != 1:
                row_values.append("|")  # vertical separator

            for n in numbers:
                if model[vv[f"x_{i}{j}{n}"]].is_true():
                    row_values.append(str(n))
                    break

        print(" ".join(row_values))

# Bool var
# x_{i}{j}{n}
vv = {
    f"x_{i}{j}{n}" : Symbol(f"x_{i}{j}{n}", BOOL)
    for i in numbers
    for j in numbers
    for n in numbers
}

# every number is conatained exactly once in every row 
for n in numbers:
    for i in numbers:
        assertions.append(ExactlyOne(vv[f"x_{i}{j}{n}"] for j in numbers))

# every number is conatained exactly once in every col 
for n in numbers:
    for j in numbers:
        assertions.append(ExactlyOne(vv[f"x_{i}{j}{n}"] for i in numbers))

# every number is contained exactly once in every square
for n in numbers:
    for top in numbers[0::3]:
        for left in numbers[0::3]:
            assertions.append(
                ExactlyOne(vv[f"x_{i}{j}{n}"]
                           for i in range(top, top+3)
                           for j in range(left, left+3))
            )

# every cell contains exactly one number
for i in numbers:
    for j in numbers:
        assertions.append(ExactlyOne(vv[f"x_{i}{j}{n}"] for n in numbers))

# Extra rule for Diagonal Sudoku
# the two main Diagonals must contain the numbers from 1 to 9
# First Diagonal
for n in numbers:
    assertions.append(
        ExactlyOne(vv[f"x_{i}{i}{n}"] for i in numbers)
    )

# Second Diagonal
for n in numbers:
    assertions.append(
        ExactlyOne(vv[f"x_{i}{10 - i}{n}"] for i in numbers)
    )

# Known numbers
assertions += [
    vv[f"x_135"],
    vv[f"x_171"],
    vv[f"x_244"],
    vv[f"x_259"],
    vv[f"x_262"],
    vv[f"x_319"],
    vv[f"x_393"],
    vv[f"x_423"],
    vv[f"x_486"],
    vv[f"x_529"],
    vv[f"x_581"],
    vv[f"x_622"],
    vv[f"x_687"],
    vv[f"x_711"],
    vv[f"x_798"],
    vv[f"x_846"],
    vv[f"x_858"],
    vv[f"x_867"],
    vv[f"x_933"],
    vv[f"x_974"],
]

# This is the Solution
# 2 6 5 | 8 7 3 | 1 4 9
# 3 1 7 | 4 9 2 | 5 8 6
# 9 4 8 | 1 5 6 | 7 2 3
# ---------------------
# 7 3 4 | 9 2 1 | 8 6 5
# 5 9 6 | 7 4 8 | 3 1 2
# 8 2 1 | 3 6 5 | 9 7 4
# ---------------------
# 1 7 2 | 5 3 4 | 6 9 8
# 4 5 9 | 6 8 7 | 2 3 1
# 6 8 3 | 2 1 9 | 4 5 7

with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")
        model = msat.get_model()
        print_sudoku(model, vv)
    else:
        print("No solution found!")


