-- SCAFFOLD: B3 O3 root count. Uncompiled statement registration only.
-- Lean and Lake are unavailable in this environment. Every proof below is open
-- in the formal track. The exact informal proof is in candidate_proof.md.
import Mathlib

noncomputable section
namespace B3O3

def E (y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos y, Real.sin y; -Real.sin y, Real.cos y]

def C (s y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![(Real.cos y)^2 - s⁻¹ * (Real.sin y)^2,
      (1 + s⁻¹) * Real.cos y * Real.sin y;
      -(1 + s) * Real.cos y * Real.sin y,
      (Real.cos y)^2 - s * (Real.sin y)^2]

def G (n : ℕ) (s y : ℝ) : ℝ := (E y * (C s y)^n) 0 1

def Q (n : ℕ) (s x : ℝ) : ℝ :=
  G n s (Real.arccos x) / Real.sqrt (1 - x^2)

def interiorZeros (n : ℕ) (s : ℝ) : Set ℝ :=
  {y | 0 < y ∧ y < Real.pi ∧ G n s y = 0}

-- O1: exact polynomial extension and degree.
theorem polynomial_extension (n : ℕ) (s : ℝ) (hn : 1 ≤ n) (hs : 1 < s) :
    ∃ p : Polynomial ℝ, p.natDegree = 2*n ∧
      ∀ x : ℝ, -1 < x → x < 1 → p.eval x = Q n s x := by
  sorry

-- O3: finite root set and exact count, with the original R parameter.
theorem root_count (n : ℕ) (R : ℝ) (hn : 1 ≤ n) (hR : 1 < R) :
    (interiorZeros n (Real.sqrt R)).Finite ∧
      (interiorZeros n (Real.sqrt R)).ncard = 2*n := by
  sorry

-- O3: all interior roots are simple.
theorem root_simple (n : ℕ) (R y : ℝ) (hn : 1 ≤ n) (hR : 1 < R)
    (hy : y ∈ interiorZeros n (Real.sqrt R)) :
    deriv (G n (Real.sqrt R)) y ≠ 0 := by
  sorry

-- O4: midpoint and equality boundary.
theorem midpoint (n : ℕ) (s : ℝ) (hs : 0 < s) :
    G n s (Real.pi / 2) = (-s)^n := by
  sorry

theorem equal_density (n : ℕ) (y : ℝ) :
    G n 1 y = Real.sin (((2*n + 1 : ℕ) : ℝ) * y) := by
  sorry

end B3O3
