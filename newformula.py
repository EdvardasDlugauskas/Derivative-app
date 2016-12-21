# -*- coding: utf-8 -*-
import sympy
from decimal import Decimal


DELTA_PREFIX = "Δ"


def partial_derivatives(expression, all_symbols):
    lst = []
    for sympy_symb in all_symbols:
        lst.append(sympy.diff(expression, sympy_symb))

    return lst


def indirect_observation_error(derivatives, deltas):
    answer = sympy.sqrt(sum((derivative * delta) ** 2 for derivative, delta in zip(derivatives, deltas)))
    return answer


def smallest(values):
    return min([Decimal(str(x)).as_tuple().exponent for x in values]) * -1

def all_delta_nondelta(expression):
    non_delta_symb = []
    delta_symb = []
    for x in sympy.S(expression).atoms(sympy.Symbol):
        non_delta_symb.append(x)
        delta_symb.append(sympy.Symbol(DELTA_PREFIX + str(x)))

    all_symb = non_delta_symb + delta_symb

    return all_symb, delta_symb, non_delta_symb

if __name__ == "__main__":
    while True:
        try:
            formula = sympy.S(input("Enter your formula: "))
        except SyntaxError as e:
            print("Could not understand formula:", e)
            continue

        non_delta_symb = []
        delta_symb = []
        for x in formula.atoms(sympy.Symbol):
            non_delta_symb.append(x)
            delta_symb.append(sympy.Symbol(DELTA_PREFIX + str(x)))

        all_symb = non_delta_symb + delta_symb

        three_derivs = partial_derivatives(formula, non_delta_symb)
        with_deltas = indirect_observation_error(three_derivs, delta_symb)

        subs = {}
        for sympy_symbol in all_symb:
            value = input("Enter value for " + str(sympy_symbol) + ": ").replace(",", ".")
            subs[sympy_symbol] = value

        sympy.pprint(with_deltas)
        result = with_deltas.subs(subs).evalf()
        print()
        try:
            print('The indirect observation error is: {0:.20f}'.format(result))
        except TypeError as e:
            print(result)
            print("Could not get a number as an answer. Did you enter everything correctly?")
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
