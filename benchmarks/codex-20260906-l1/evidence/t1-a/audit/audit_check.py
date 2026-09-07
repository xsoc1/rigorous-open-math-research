"""Exact algebra checks for this audit; Python 3 standard library only.

Arithmetic is in Q[s, s^-1, c, q]/(q^2 + c^2 - 1). These checks
support the written audit; they do not automate its uniform root-count proof.
"""

import json
from fractions import Fraction
from math import comb


class P:
    def __init__(self, value=0):
        terms = value if isinstance(value, dict) else {(0, 0, 0): value}
        self.terms = {key: Fraction(val) for key, val in terms.items() if val}

    @staticmethod
    def coerce(value):
        return value if isinstance(value, P) else P(value)

    def __add__(self, other):
        result = dict(self.terms)
        for key, val in self.coerce(other).terms.items():
            result[key] = result.get(key, 0) + val
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({key: -val for key, val in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        result = {}
        for (sc1, cc1, qc1), val1 in self.terms.items():
            for (sc2, cc2, qc2), val2 in self.coerce(other).terms.items():
                pairs, remaining_q = divmod(qc1 + qc2, 2)
                for j in range(pairs + 1):
                    key = (sc1 + sc2, cc1 + cc2 + 2 * j, remaining_q)
                    val = val1 * val2 * comb(pairs, j) * (-1) ** j
                    result[key] = result.get(key, 0) + val
        return P(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = P(1)
        for _ in range(exponent):
            result *= self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def at_cq(self, c_value, q_value):
        result = P(0)
        for (sc, cc, qc), val in self.terms.items():
            result += P({(sc, 0, 0): val * c_value ** cc * q_value ** qc})
        return result

    def at_s_one(self):
        result = P(0)
        for (_, cc, qc), val in self.terms.items():
            result += P({(0, cc, qc): val})
        return result

    def derivative_c(self):
        assert all(qc == 0 for _, _, qc in self.terms)
        return P({(sc, cc - 1, 0): val * cc
                  for (sc, cc, _), val in self.terms.items() if cc})


def mm(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def at_cq(matrix, cv, qv):
    return [[entry.at_cq(cv, qv) for entry in row] for row in matrix]


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "result": "PASS"})


s = P({(1, 0, 0): 1})
r = P({(-1, 0, 0): 1})
c = P({(0, 1, 0): 1})
q = P({(0, 0, 1): 1})
a = s + 2 + r
z = (a * c ** 2 - s - r) * Fraction(1, 2)
E = [[c, q], [-q, c]]
C = [[c ** 2 - r * q ** 2, (1 + r) * c * q],
     [-(1 + s) * c * q, c ** 2 - s * q ** 2]]
I = [[P(1), P(0)], [P(0), P(1)]]

check("circle relation and reciprocal parameter", c ** 2 + q ** 2 == 1 and s * r == 1)
check("a = (s+1)^2/s", a * s == (s + 1) ** 2)
check("two formulas for z", z == 1 - a * (1 - c ** 2) * Fraction(1, 2))
check("det C = 1", C[0][0] * C[1][1] - C[0][1] * C[1][0] == 1)
check("trace C = 2z", C[0][0] + C[1][1] == 2 * z)
C2 = mm(C, C)
check("matrix recurrence identity C^2 - 2z C + I = 0",
      all(C2[i][j] - 2 * z * C[i][j] + I[i][j] == 0
          for i in range(2) for j in range(2)))
check("G_0 = q", E[0][1] == q)
check("G_1 = q(a c^2 - s) = q(2z+r)",
      mm(E, C)[0][1] == q * (a * c ** 2 - s) == q * (2 * z + r))
check("z'(x) = ax", z.derivative_c() == a * c)
check("s+r-2 = (s-1)^2/s", s * (s + r - 2) == (s - 1) ** 2)
check("n=1 roots after clearing (s+1)^2", a * s ** 2 - s * (s + 1) ** 2 == 0)
check("z(1) = z(-1) = 1", z.at_cq(1, 0) == z.at_cq(-1, 0) == 1)
check("y=0 matrices", at_cq(C, 1, 0) == I and at_cq(E, 1, 0) == I)
check("y=pi matrices", at_cq(C, -1, 0) == I and
      at_cq(E, -1, 0) == [[-P(1), P(0)], [P(0), -P(1)]])
check("midpoint matrices", at_cq(C, 0, 1) == [[-r, P(0)], [P(0), -s]] and
      at_cq(E, 0, 1) == [[P(0), P(1)], [-P(1), P(0)]])
check("R=1 matrix identity C_1 = E^2",
      [[entry.at_s_one() for entry in row] for row in C] == mm(E, E))

print(json.dumps({
    "method": "Exact rational Laurent-polynomial arithmetic; no numerical sampling",
    "scope": "Algebraic identities only; induction, signs, counts, and simplicity are checked in the audit",
    "checks": checks,
    "passed": len(checks)
}, indent=2))
