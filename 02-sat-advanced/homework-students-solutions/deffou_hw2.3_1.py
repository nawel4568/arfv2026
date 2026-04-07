from pysmt.shortcuts import And, Or, ExactlyOne, Solver, Symbol, BOOL, Implies

# Here is the puzzle i got
# https://logic.puzzlebaron.com/play.php?u2=37a54c20ce691d7a5230d701dac6608e

def print_model(model):
    for m in months:
        country = [
            cname for c, cname in countries.items() if model[month_country[f"c_{m}_{c}"]].is_true()
        ][0]
        exhibit = [
            ename for e, ename in exhibits.items() if model[month_exhibit[f"e_{m}_{e}"]].is_true()
        ][0]
        print(f" {m}: The presentation from {country} is the {exhibit}")


months = ["Jan", "Feb", "Mar", "Apr"]
exhibits = {
    "b": "basketry",
    "g": "glassware",
    "l": "lacquerware",
    "s": "sculpture",
}
countries = {
    "A": "Azerbaijan",
    "G": "Gabon",
    "N": "Norway",
    "U": "Uganda",
}

month_exhibit = {f"e_{i}_{j}": Symbol(f"e_{i}_{j}", BOOL) for i in months for j in exhibits}
month_country = {f"c_{i}_{j}": Symbol(f"c_{i}_{j}", BOOL) for i in months for j in countries}

assertions = []

# The lacquerware exhibit took place in April
assertions.append(
    month_exhibit["e_Apr_l"]
)

# The presentation from Uganda is either the basketry presentation or the lacquerware presentation
for m in months:
    assertions.append(
        Implies(
            month_country[f"c_{m}_U"],
            Or(
                month_exhibit[f"e_{m}_b"],
                month_exhibit[f"e_{m}_l"]
            )
        )
    )

# The glassware exhibit took place in February
assertions.append(month_exhibit["e_Feb_g"])

# February's exhibit is either the presentation from Azerbaijan or the presentation from Norway.
assertions.append(
    Or(month_country["c_Feb_A"], month_country["c_Feb_N"])
)

# The sculpture presentation was held 2 months after the presentation from Norway
assertions.append(
    Or(
        And(month_country["c_Jan_N"], month_exhibit["e_Mar_s"]),
        And(month_country["c_Feb_N"], month_exhibit["e_Apr_s"])
    )
)

# Hidden condition: every month, there is a presentation in exactly one country
for m in months:
    assertions.append(ExactlyOne(month_country[f"c_{m}_{c}"] for c in countries))

# Hidden condition: each country has an presentation in only one month
for c in countries:
    assertions.append(ExactlyOne(month_country[f"c_{m}_{c}"] for m in months))

# Hidden condition: every month, there is a presentation for exactly one exhibit
for m in months:
    assertions.append(ExactlyOne(month_exhibit[f"e_{m}_{e}"] for e in exhibits))

# Hidden condition: each exhibit appears once
for e in exhibits:
    assertions.append(ExactlyOne(month_exhibit[f"e_{m}_{e}"] for m in months))

with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")

        msat_model = msat.get_model()
        print_model(msat_model)
    else:
        print("No solution exists")
