# Frozen calibration task: B3 O3 root count

Source: user statement in this run; copied without consulting any other source.

Let n>=1 be an integer and R>1. Set s=sqrt(R). For real y write c=cos(y), q=sin(y), and define

```text
E(y)=[[c,q],[-q,c]],
C_s(y)=[[c^2-s^(-1)q^2,(1+s^(-1))cq],[-(1+s)cq,c^2-sq^2]],
M_{n,s}(y)=E(y)C_s(y)^n,
G_{n,s}(y)=(M_{n,s}(y))_{12}.
```

These are normalized transfer matrices for the Dirichlet problem -u''=lambda rho(x)u, u(0)=u(1)=0, with balanced alternating density [1,R,1,R,...,1] consisting of 2n+1 blocks. The 1-blocks have length st, the R-blocks have length t, t=1/((n+1)s+n), and y=sqrt(lambda)st.

Prove or disprove: for every n>=1 and R>1, G has exactly 2n zeros in (0,pi), all simple.

An equivalent polynomial formulation may be used only if justified. For x in (-1,1), define Q_{n,s}(x)=G_{n,s}(arccos(x))/sqrt(1-x^2). Prove any claimed polynomial extension, degree, root location, and simplicity. Audit n=1, y=0, y=pi, y=pi/2, and boundary R=1 separately. Do not count endpoint zeros. Numerical scans, finitely many n/R, pairing without a count, or a degree bound without location and simplicity do not complete the task. State every external theorem with hypotheses. If incomplete, return the strongest exact partial result and first unresolved obligation without claiming completion.
