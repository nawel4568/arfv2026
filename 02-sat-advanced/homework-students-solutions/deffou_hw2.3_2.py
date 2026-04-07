from pysmt.shortcuts import And, Or, Not, Iff, ExactlyOne, Solver, Symbol, BOOL, Implies

# Define the escape sequences
BOLD = "\033[1m"
RESET = "\033[0m"

# Here is the puzzle i got
# https://logic.puzzlebaron.com/play.php?u2=d786159bebfccd342a3eeb7ab8991b3c

def print_model(model):
    for d in dates:
        string = [
            snumber for snumber in strings if model[date_string[f"s_{d}_{snumber}"]].is_true()
        ][0]
        wood_type = [
            wtype for w, wtype in wood_types.items() if model[date_wood[f"w_{d}_{w}"]].is_true()
        ][0]
        print(f" {BOLD}{d}{RESET}: an instrument of {BOLD}{string}{RESET} strings was built using {BOLD}{wood_type}{RESET} wood type")

dates = [1720, 1745, 1770, 1795, 1820]
strings = [26, 30, 34, 38, 46]
wood_types = {
    "a": "ash",
    "o": "oak",
    "r": "rosewood",
    "s": "spruce",
    "w": "walnut"
}

date_string = {f"s_{i}_{j}": Symbol(f"s_{i}_{j}", BOOL) for i in dates for j in strings}
date_wood = {f"w_{i}_{j}": Symbol(f"w_{i}_{j}", BOOL) for i in dates for j in wood_types}

assertions = []

# The harp built in 1745 was either the spruce instrument or the instrument with 26 strings.
assertions.append(Or(
    date_wood["w_1745_s"],
    date_string["s_1745_26"]
))

# The instrument with 26 strings wasn't built in 1820.
assertions.append(Not(date_string["s_1820_26"]))

# The instrument with 30 strings was built 25 years before the spruce harp.

assertions.append(Or(
    And(
        date_string[f"s_{date}_30"], 
        date_wood[f"w_{date+25}_s"]
        )
        for date in dates[:-1]
))

# The instrument with 26 strings is made from ash.
assertions.append(Or(
    And(
        date_string[f"s_{date}_26"], 
        date_wood[f"w_{date}_a"]
    )
        for date in dates
))

# The spruce instrument was built 25 years before the rosewood harp.
assertions.append(Or(
    And(
        date_wood[f"w_{date}_s"], 
        date_wood[f"w_{date+25}_r"]
    )
    for date in dates[:-1]
))

# The instrument with 46 strings was built somewhat after the harp with 30 strings.
assertions.append(Or(
    And(
        date_string[f"s_{i}_46"],
        date_string[f"s_{j}_30"]
    )
    for i in dates
    for j in dates
    if j < i
))

# The walnut harp was built somewhat after the instrument with 46 strings.
assertions.append(Or(
    And(
        date_wood[f"w_{i}_w"],
        date_string[f"s_{j}_46"]
    )
    for i in dates
    for j in dates
    if j < i
))

# The harp with 34 strings was built 25 years after the harp with 30 strings.
assertions.append(Or(
    And(
        date_string[f"s_{date}_30"], 
        date_string[f"s_{date+25}_34"]
    )
    for date in dates[:-1]
))

# Hidden conditions: every dates there was built exactly one instrument with one wood type
for d in dates:
    assertions.append(ExactlyOne(date_wood[f"w_{d}_{i}"] for i in wood_types))

# Hidden conditions: each wood type was used in exactly one date
for i in wood_types:
    assertions.append(ExactlyOne(date_wood[f"w_{d}_{i}"] for d in dates))

# Hidden conditions: every dates there was built exactly one instrument with one string number
for d in dates:
    assertions.append(ExactlyOne(date_string[f"s_{d}_{i}"] for i in strings))
    
# Hidden conditions: one instrument with one string number was built in exactly one date
for i in strings:
    assertions.append(ExactlyOne(date_string[f"s_{d}_{i}"] for d in dates))



with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")
        msat_model = msat.get_model()
        print_model(msat_model)
    else:
        print("No solution exists")
