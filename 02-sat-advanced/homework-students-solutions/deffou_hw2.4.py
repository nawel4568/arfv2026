from pysmt.shortcuts import And, Or,Not, ExactlyOne, Solver, Symbol, BOOL, Implies

N = list(range(1, 9))

def print_chessboard(model, chessboard):
    size = len(N)
    print("+" + "---+" * size)
    for i in N:
        row_values = []
        for j in N:
            var_key = f"x_{i}_{j}"
            if model[chessboard[var_key]].is_true():
                row_values.append(" Q ")
            else:
                row_values.append(" . ")
        print("|" + "|".join(row_values) + "|")
        print("+" + "---+" * size)

# a chess board with N=8, if x_1_1 is True means the queen is there else the square is empty
chessboard = {f"x_{i}_{j}": Symbol(f"x_{i}_{j}", BOOL) for i in N for j in N}

assertions = []

# every row have exactly one queen
for i in N:
    assertions.append(
        ExactlyOne(chessboard[f"x_{i}_{j}"] for j in N)
    )

# every column have exactly one queen
for j in N:
    assertions.append(
        ExactlyOne(chessboard[f"x_{i}_{j}"] for i in N)
    )


# if a queen is in x_{i}_{j} then all diagonal squares should be empty
for i in N:
    for j in N:
        pos_diag = []
        neg_diag = []
        for k in range(0, 8):
            if i+k == i and j+k == j:
                continue
            if i+k<9 and j+k<9:
                pos_diag.append(chessboard[f"x_{i+k}_{j+k}"])
            if i-k>0 and j+k<9:
                neg_diag.append(chessboard[f"x_{i-k}_{j+k}"])

        assertions.append(
            Implies(
                chessboard[f"x_{i}_{j}"],
                Not(Or(neg_diag+pos_diag))
            )
        )


# The Output for a 8x8
# +---+---+---+---+---+---+---+---+
# | . | . | . | . | . | Q | . | . |
# +---+---+---+---+---+---+---+---+
# | . | . | . | . | . | . | . | Q |
# +---+---+---+---+---+---+---+---+
# | . | Q | . | . | . | . | . | . |
# +---+---+---+---+---+---+---+---+
# | . | . | . | Q | . | . | . | . |
# +---+---+---+---+---+---+---+---+
# | Q | . | . | . | . | . | . | . |
# +---+---+---+---+---+---+---+---+
# | . | . | . | . | . | . | Q | . |
# +---+---+---+---+---+---+---+---+
# | . | . | . | . | Q | . | . | . |
# +---+---+---+---+---+---+---+---+
# | . | . | Q | . | . | . | . | . |
# +---+---+---+---+---+---+---+---+

# Check the uiquness of the output
# It is not Unique
assertions.append(
    Not(
        And(
            chessboard[f"x_1_6"],
            chessboard[f"x_2_8"],
            chessboard[f"x_3_2"],
            chessboard[f"x_4_4"],
            chessboard[f"x_5_1"],
            chessboard[f"x_6_7"],
            chessboard[f"x_7_5"],
            chessboard[f"x_8_3"],
        )
    )
)

with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")
        model = msat.get_model()
        print_chessboard(model, chessboard)
    else:
        print("No solution found!")
