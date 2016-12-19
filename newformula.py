from sympy import *

def partial_derivatives(expression, all_symbols):
    lst = []
    for symb in all_symbols:
        lst.append(diff(expression, symb))

    return lst

def indirect_observation_error(isvestines, deltas):
    answ = sqrt(sum((isvestine*delta)**2 for isvestine, delta in zip(isvestines, deltas)))
    return answ

while True:
    try:
        formula = S(input("Enter your formula: "))
    except SyntaxError as e:
        print("Could not understand formula:", e)
        continue

    non_delta_symb = []
    delta_symb = []
    for x in formula.atoms(Symbol):
        non_delta_symb.append(x)
        delta_symb.append(Symbol("d_" + str(x)))

    all_symb = non_delta_symb + delta_symb

    three_derivs = partial_derivatives(formula, non_delta_symb)
    with_deltas = indirect_observation_error(three_derivs, delta_symb)

    subs = {}
    for symb in all_symb:
        value = input("Enter value for " + str(symb) + ": ").replace(",", ".")
        subs[symb] = value

    pprint(with_deltas)
    result = with_deltas.subs(subs)
    print()
    try:
        print('Answ: {0:.20f}'.format(result))
    except TypeError as e:
        print("Could not get an answer. Did you enter everything correctly? Please try again")
    print()






"""
h, R, t = symbols("h R t")
dh, dR, dt = symbols("dh dR dt")
form2 = (2*h)/(R*t**2)
form2isvest = daline_isvestine_1(form2, [h, R, t])
got2 = daline_isvestine_2(form2isvest, [dh, dR, dt])
got2subbed = got2.subs([(h, 0.711), (R, 0.025), (t, 6.319), (dh, 0.001), (dR, 0.001), (dt, 0.01)])
print("Answ:", got2subbed)
"""