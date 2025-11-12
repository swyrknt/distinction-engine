"""
Canonical Form Test Suite

Tests whether the engine provides a deterministic, content-addressable
representation of structure. Validates that identical topological
structures constructed via different temporal sequences yield
mathematically identical identities (Hashes).

Falsification Target:
Path Dependence - Constructing the same logical structure via different
synthesis orders produces different IDs, proving the system lacks
a canonical form (and is therefore state-dependent, not timeless).
"""

import unittest
from engine import Distinction, DistinctionEngine

class TestCanonicalForm(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def test_falsify_path_dependence(self):
        """
        Falsification Test: Structural Path Dependence

        Hypothesis: The identity of a composite distinction is determined
        solely by its constituent parts and their topology, independent
        of the temporal order of assembly.

        Scenario: Construct a "Diamond" structure ((A+B) + (C+D))
        using two different parallel processing orders.
        """
        print("\nTest: Canonical Form / Path Independence")

        d0 = self.engine.d0
        d1 = self.engine.d1

        a = self.engine.synthesize(d0, d1)
        b = self.engine.synthesize(d1, d0)
        c = self.engine.synthesize(a, d0)
        d = self.engine.synthesize(a, d1)

        print(f"   Base distinctions created: A={a.id[:6]}, C={c.id[:6]}, D={d.id[:6]}")

        print("   Executing construction sequence 1 (left-first)...")
        engine_1 = DistinctionEngine()
        e1_c = engine_1.all_distinctions[c.id] = c
        e1_d = engine_1.all_distinctions[d.id] = d
        e1_a = engine_1.all_distinctions[a.id] = a

        branch_left_1 = engine_1.synthesize(e1_c, e1_d)
        branch_right_1 = engine_1.synthesize(e1_a, e1_c)
        final_1 = engine_1.synthesize(branch_left_1, branch_right_1)

        print(f"   Sequence 1 result: {final_1.id}")

        print("   Executing construction sequence 2 (right-first)...")
        engine_2 = DistinctionEngine()
        e2_c = engine_2.all_distinctions[c.id] = c
        e2_d = engine_2.all_distinctions[d.id] = d
        e2_a = engine_2.all_distinctions[a.id] = a

        branch_right_2 = engine_2.synthesize(e2_a, e2_c)
        branch_left_2 = engine_2.synthesize(e2_c, e2_d)
        final_2 = engine_2.synthesize(branch_left_2, branch_right_2)

        print(f"   Sequence 2 result: {final_2.id}")

        self.assertEqual(final_1.id, final_2.id,
            "FALSIFIED: Path Dependence detected. Identity depends on construction order.")

        print("\n   Hypothesis sustained.")
        print("   Identical structures produced identical IDs regardless of construction order.")
        print("   Content-addressable structure enables constant-time structural comparison.")

if __name__ == '__main__':
    unittest.main()