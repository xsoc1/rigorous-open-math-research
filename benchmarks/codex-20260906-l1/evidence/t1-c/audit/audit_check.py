"""Exact supplementary algebra checks; the uniform root proof is audited in audit.json.

Run with Python 3 and its standard library only. No input beyond the formulas in
TASK.md and CANDIDATE.md is used. Polynomials are Laurent polynomials in s and
ordinary polynomials in c,q, reduced using q^2 = 1-c^2. Thus these checks are
symbolic identities, not numerical samples or a substitute for the root proof.
"""

from math import comb
import json


class P:
    def __init__(self, terms=0):
        if isinstance(terms, int):
            terms = {(0, 0, 0): terms}
        result = {}
        for (s, c, q), coefficient in terms.items():
            pairs, remainder = divmod(q, 2)
            for j in range(pairs + 1):
                key = (s, c + 2 * j, remainder)
                result[key] = result.get(key, 0) + coefficient * comb(pairs, j) * (-1) ** j
        self.terms = {key: value for key, value in result.items() if value}

    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = dict(self.terms)
        for key, value in other.terms.items():
            result[key] = result.get(key, 0) + value
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -(other if isinstance(other, P) else P(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = {}
        for left, lv in self.terms.items():
            for right, rv in other.terms.items():
                key = tuple(a + b for a, b in zip(left, right))
                result[key] = result.get(key, 0) + lv * rv
        return P(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = P(1)
        for _ in range(exponent):
            result = result * self
        return result


def matrix_multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


checks = []


def check(name, actual, expected):
    if isinstance(actual, list):
        difference = [(actual[i][j] - expected[i][j]).terms
                      for i in range(2) for j in range(2)]
    else:
        difference = [(actual - expected).terms]
    assert not any(difference), (name, difference)
    checks.append(name)


def at_cq(poly, c_value, q_value):
    result = P()
    for (se, ce, qe), coefficient in poly.terms.items():
        result += P({(se, 0, 0): coefficient * c_value ** ce * q_value ** qe})
    return result


def at_s_one(poly):
    result = P()
    for (_, ce, qe), coefficient in poly.terms.items():
        result += P({(0, ce, qe): coefficient})
    return result


s = P({(1, 0, 0): 1})
a = P({(-1, 0, 0): 1})
c = P({(0, 1, 0): 1})
q = P({(0, 0, 1): 1})
identity = [[P(1), P()], [P(), P(1)]]
e = [[c, q], [-q, c]]
matrix = [[c*c - a*q*q, (1+a)*c*q],
          [-(1+s)*c*q, c*c - s*q*q]]
trace = matrix[0][0] + matrix[1][1]
determinant = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
twice_a_capital = s + 2 + a
twice_z = 2 - twice_a_capital*q*q

check("det C = 1", determinant, 1)
check("tr C = 2z", trace, twice_z)
squared = matrix_multiply(matrix, matrix)
check("C^2 - 2z C + I = 0",
      [[squared[i][j] - twice_z*matrix[i][j] + identity[i][j]
        for j in range(2)] for i in range(2)], [[P(), P()], [P(), P()]])
g_one = matrix_multiply(e, matrix)[0][1]
check("G_1 = q(2z+a)", g_one, q*(twice_z+a))
check("n=1 explicit formula", g_one, q*(twice_a_capital*c*c-s))
check("2A = (s+1)^2/s", twice_a_capital, (s+1)**2*a)
check("A-2 = (s-1)^2/(2s)", twice_a_capital-4, (s-1)**2*a)
check("(A-2)/A = (s-1)^2/(s+1)^2",
      (twice_a_capital-4)*(s+1)**2, twice_a_capital*(s-1)**2)
check("C(0) = I", [[at_cq(p, 1, 0) for p in row] for row in matrix], identity)
check("E(0) = I", [[at_cq(p, 1, 0) for p in row] for row in e], identity)
check("C(pi) = I", [[at_cq(p, -1, 0) for p in row] for row in matrix], identity)
check("E(pi) = -I", [[at_cq(p, -1, 0) for p in row] for row in e],
      [[-p for p in row] for row in identity])
check("C(pi/2) = diag(-1/s,-s)",
      [[at_cq(p, 0, 1) for p in row] for row in matrix], [[-a, P()], [P(), -s]])
check("E(pi/2) = [[0,1],[-1,0]]",
      [[at_cq(p, 0, 1) for p in row] for row in e], [[P(), P(1)], [P(-1), P()]])
check("C_1(y) = E(2y)", [[at_s_one(p) for p in row] for row in matrix],
      [[c*c-q*q, 2*c*q], [-2*c*q, c*c-q*q]])

print(json.dumps({"passed": len(checks), "checks": checks}, indent=2))
